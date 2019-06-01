require(['jquery'], function ($) {
    $(document).ready(function (e) {
        let request_uri = window.location.href.replace(window.location.protocol + "//" + window.location.host, "");
        let active_ele = $("a[href='" + request_uri + "']");

        /** Add Active State to Current Page Link */
        active_ele.parent("li").addClass("active");
        processActiveState(active_ele);

        /** Bind Dropdown Links **/
        function processActiveState(ele) {
            if (ele.hasClass("single"))
                return

            if (ele.parents(".sidebar-dropdown").hasClass("active")){
                ele.parents(".sidebar-dropdown").removeClass("active")
                if (!$(".page-main").hasClass("toggled")) {
                    showSidebar(ele.parents(".sidebar-dropdown"));
                }
            }
                
            else {
                $(".sidebar-dropdown.active").removeClass("active");
                if (!$(".page-main").hasClass("toggled")) {
                    showSidebar(ele.parents(".sidebar-dropdown"));
                } else {
                    ele.parents(".sidebar-dropdown").addClass("active");
                }

            }
        }

        $(".dropdown-icon, .sidebar-dropdown>a").click(function (e) {
            if($(this).hasClass('single'))
                return
            e.preventDefault();
            processActiveState($(this));
        });

        /** Bind Toggle Sidebar */
        
        function showSidebar(active) {
            let ele = $(".page-main");
            active.removeClass('active');
            $(".user-info").hide();
            setTimeout(function () {
                ele.addClass("toggled");
                $('.toggle-sidebar').find(".toggle-icon").css("transform", "rotate(0deg)");
                setTimeout(function () {
                    active.addClass("active");
                    $(".user-info").fadeIn();
                }, 500);
            }, 500);
        }

        $(".toggle-sidebar").click(function (e) {
            e.preventDefault();
            let ele = $(".page-main");
            let active = $(".sidebar-dropdown.active");
            if (ele.hasClass("toggled")) {
                ele.removeClass("toggled")
                $(this).find(".toggle-icon").css("transform", "rotate(180deg)");
            } else {
                showSidebar(active);
            }
        });
        
        
        /** Hide Preloader **/
        $("#preloader").fadeOut(300);
    });
});