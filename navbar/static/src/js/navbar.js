/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var ExampleWidget = Widget.extend({
   template: 'LoginNav',
   events: {
       'click #create_so': '_onClick',
   },
   _onClick: function(){
       this.do_action({
            type: 'ir.actions.act_window',
            name: 'navbar login',
            res_model: 'navbar.login',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
       });
   },
});
SystrayMenu.Items.push(ExampleWidget);
export default ExampleWidget;