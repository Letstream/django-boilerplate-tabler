import re
from django.utils import timezone
from django.shortcuts import reverse

class TableData:

    fields = []
    rows = []

    def __init__(self):
        self.meta = {}
        self.fields = []
        self.available_fields = []
        self.enabled_fields = []
        self.sortable_fields = []
        self.rows = []
        self.actions = []

    def addRow(self, id, grouped=1, header=False, attrs={}):
        self.rows.append({
            "id": id,
            "groups": [],
            "actions": [],
            "header": header,
            "attrs": attrs
        })

    def addGroup(self, rowIndex):
        self.rows[rowIndex]['groups'].append([])

    def addCellToRow(self, rowIndex, cell_type, text, subtext=None, meta=None, groupIndex=0):
        if len(self.rows[rowIndex]['groups']) == 0:
            self.addGroup(rowIndex)

        self.rows[rowIndex]['groups'][groupIndex].append({
            "type": cell_type,
            "text": text,
            "subtext": subtext,
            "meta": meta
        })

    def addActionButtonToRow(self, rowIndex, url, label, btn_class, add_next=False, open_in_new=False, data_toggle=False):
        self.rows[rowIndex]['actions'].append({
            'url': url,
            'label': label,
            'btn_class': btn_class,
            'add_next': add_next,
            'open_in_new': open_in_new,
            'data_toggle' : data_toggle
        })

    def addField(self, field, label, field_class=None):
        self.fields.append({
            "name": field,
            "class": field_class,
            "label": label
        })
        self.enabled_fields.append(field)

    def addAvailableField(self, field, field_label):
        self.available_fields.append({
            "name": field,
            "label": field_label
        })
    
    def addSortableField(self, field, field_label):
        self.sortable_fields.append({
            "name": field,
            "label": field_label
        })
    
    def addMetaField(self, key, value):
        self.meta[key] = value

    def addActionButton(self, label, url, css_class="btn-primary", icon=None):
        self.actions.append({
            "label": label,
            "url": url,
            "css_class": css_class,
            "icon": icon
        })

    def getPaginationUrl(self, request_obj):
        if "pagination" not in self.meta:
            return None
        
        next = None
        prev = None
        pagination = self.meta['pagination']
        if (pagination['start']-1) != 0:
            if "page=" in request_obj:
                prev = "?%s" % re.sub(r"page=[0-9]{1,}", "page=%s" % (pagination['page']-1), request_obj)
            else:
                prev = "?page=%s&%s" % (pagination['page']-1, request_obj)
            
            if "pagesize=" in prev:
                prev =  re.sub(r"pagesize=[0-9]{1,}", "pagesize=%s" % pagination['page_size'], prev)
            else:
                prev = "%s&pagesize=%s" % (prev, pagination['page_size'])

        if pagination['end'] < pagination['total']:
            if "page=" in request_obj:
                next = "?%s" % re.sub(r"page=[0-9]{1,}", "page=%s" % (pagination['page']+1), request_obj)
            else:
                next = "?page=%s&%s" % (pagination['page']+1, request_obj)
            
            if "pagesize=" in next:
                next =  re.sub(r"pagesize=[0-9]{1,}", "pagesize=%s" % pagination['page_size'], next)
            else:
                next = "%s&pagesize=%s" % (next, pagination['page_size'])
        
        return prev, next         

    def getObject(self):
        return {
            "fields": self.fields,
            "available_fields": self.available_fields,
            "enabled_fields": self.enabled_fields,
            "sortable_fields": self.sortable_fields,
            "rows": self.rows,
            "meta": self.meta,
            "actions": self.actions
        }
    
    class PageIndexOutOfRangeError(Exception):
        pass
