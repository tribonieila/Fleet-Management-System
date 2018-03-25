#-*- encoding:utf-8 -*- # * formModal
from gluon.html import A, DIV, H3, BUTTON, OPTION, TAG, I, XML
from gluon.sqlhtml import SQLFORM
from gluon.compileapp import LOAD
from gluon.http import HTTP
from gluon import current
class Modal(object):
     def __init__(self, field, value, title_btn, title_modal):
         self.field = field
         self.value = value
         self.title_btn = title_btn
         self.title_modal = title_modal
         self.key = str(self.field).replace('.', '_')
         self.modal_id = 'modal_%s' % self.key
         self._target = "c_" + self.key
         self.request = current.request
         self.response = current.response
         self.session = current.session

     def btn_show(self):
         # Button to trigger modal .
        btn_show_modal = A(I(_class="icon-plus-sign"),
                             ' ', self.value,
                             **{"_role": "button",
                                #"_class": "btn btn-link",
                               "_data-toggle": "modal",
                                "_href": "#%s" % self.modal_id,
                                "_title": self.title_btn})
        return btn_show_modal

     def div_modal(self, content_modal):

         div_modal = DIV(
                         DIV(
                             H3(self.title_modal, _id="myModalLabel"),
                             _class="modal-header"),
                         DIV(content_modal, _class="modal-body"),
                         DIV(
                             BUTTON("Cerrar", **{"_class": "btn",
                                                 "_data-dismiss": "modal",
                                                 "_aria-hidden": "true"}),
                             _class="modal-footer",
                             ),
                         **{"_id": "%s" % self.modal_id,
                            "_class": "modal hide face",
                            "_tabindex": "-1",
                            "_role": "dialog",
                            "_aria-hidden": "true",
                            "_aria-labelledby": "myModalLabel"}
                     )
         return div_modal

     def create(self):

         if not self.field.type.startswith('reference'):
             raise SyntaxError("Sólo puede usarse con field reference")
         if not hasattr(self.field.requires, 'options'):
             raise SyntaxError("No puede determinarse las opciones")
         if self.request.get_vars._ajax_add == str(self.field):
             table = self.field._db[self.field.type[10:]]
             raise HTTP(200, self.checkForm(table))
         return self.btn_show()

     def formModal(self):

         return self.div_modal(LOAD(self.request.controller,
                                     self.request.function,
                                     args=self.request.args,
                                     vars=dict(_ajax_add=self.field),
                                     target=self._target,
                                     ajax=True)
                                 )

     def checkForm(self, table):
        formnamemodal = "formmodal_%s" % self.key
        form = SQLFORM(table, formname=formnamemodal)
        if form.accepts(self.request.vars,
                         self.session,
                         formname=formnamemodal):
            options = TAG[''](*[OPTION(v,
                             _value=k,
                             _selected=str(form.vars.id) == str(k))
                             for (k, v) in self.field.requires.options()])
            _cmd = "jQuery('#%s').html('%s');"
            _cmd += "jQuery('#%s').modal('hide')"
            command = _cmd % (self.key,
                               options.xml().replace("'", "\'"),
                               self.modal_id
                              )
            self.response.flash = 'Se creó el registro'
            self.response.js = command
        elif form.errors:
            self.response.flash = "Controle el formulario"
        return form