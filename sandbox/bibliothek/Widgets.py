
from django import forms

from datetime import *

from html import escape

from django.forms.utils import flatatt
from django_filters.widgets import BooleanWidget
from django.utils.translation import gettext as _


import django.forms

from string import capwords

from django.forms import CheckboxInput, Select, SelectMultiple,NumberInput

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template import loader


class RangeInput(NumberInput):
    input_type = 'range'

    def __init__(self,**kwargs):

        self.valuemin = kwargs.pop('valuemin')
        self.valuemax = kwargs.pop('valuemax')

        self.value = kwargs.pop('value')
        self.step = kwargs.pop('step')
        return super().__init__(**kwargs)

    def render(self, name, value, attrs=None, renderer=None):

        context = self.get_context(name, value, attrs)

        context['widget']['attrs']['valuemin'] = self.valuemin
        context['widget']['attrs']['valuemax'] = self.valuemax

        context['widget']['attrs']['value'] = self.value
        context['widget']['attrs']['step'] = self.step

        template = loader.get_template('widgets/RangeWidget.html').render(context)
        return mark_safe(template)




class RangeWidget(forms.NumberInput):
    def __init__(self,**kwargs):
        self.title = kwargs.pop('title')
        self.valuemin = kwargs.pop('valuemin')
        self.valuemax = kwargs.pop('valuemax')
        self.initmin = kwargs.pop('initmin')
        self.initmax = kwargs.pop('initmax')
        self.valuenow = kwargs.pop('valuenow')
        self.eav = kwargs.pop('eav')
        return super().__init__(**kwargs)
    def render(self, name, value, attrs=None, renderer=None):

        context = self.get_context(name, value, attrs)
        context['widget']['attrs']['title'] = self.title
        context['widget']['attrs']['valuemin'] = self.valuemin
        context['widget']['attrs']['valuemax'] = self.valuemax
        context['widget']['attrs']['initmin'] = self.initmin
        context['widget']['attrs']['initmax'] = self.initmax
        context['widget']['attrs']['valuenow'] = self.valuenow
        context['widget']['attrs']['eav'] = self.eav

        template = loader.get_template('widgets/RangeWidget.html').render(context)
        return mark_safe(template)







class ChoiceWidget(django.forms.widgets.ChoiceWidget):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)
        context['widget']['nestedtree'] = eval(self.modelrelatedclass).objects.all()
        return context


class TreeCheckboxSelectMultiple(ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'django/forms/widgets/TreeCheckboxSelectMultiple.html'

    def __init__(self, modelrelatedclass, *args, **kwargs):
        self.modelrelatedclass = modelrelatedclass
        init = super().__init__(*args, **kwargs)


def getallactivefields(model, exclude):
    fieldlist = [f.fieldname for f in
                 Fieldlist.objects.filter(fieldisactive=True, modelname=model)]

    return list(set(fieldlist) - set(exclude))


selectdict = {'Historietype': {'list': ['name']}, 'Address': {'list': ['lastname']}}


class selectfilterwidget(Select):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelChoiceField
    """

    def __init__(
            self,
            exclude,

            model,
            *args,
            **kwargs
    ):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(selectfilterwidget, self).__init__(*args, **kwargs)
        self.exclude = exclude

        self.model = model

    def render(self, name, value,
               attrs=None, choices=[], **kwargs):
        if value is None:
            value = []
        if isinstance(self.choices, list):
            choices = self.choices
        else:
            choices = []

        output = []
        output.append('<div  class = "singleselecttreewidget">')
        modal_name = 'modal' + escape(name)
        modal_add_button = 'modal_add_button_' + escape(name)
        output.append('<div class = "row"><div class = "col-11"><div id="{}widget">'.format(escape(name)))
        output.append('''

	     <select name="{}" id="id_{}" class="{} select2"   style="width:50%"></select></div></div><div class = "col-1">  <button type="button" class="btn btn-info btn-lg openmodal{}" data-toggle="modal"  data-target="#{}"><i class="fas fa-link"></i></button> </div></div>
	  		<!-- Modal -->
            <div class="modal fade" id="{}" tabindex="-1" role="dialog" aria-hidden="false">
                <div class="modal-dialog modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="false">&times;</span>
                            </button>
                        </div>
                    <div class="modal-body" >'''.format(escape(name), escape(name), escape(name), escape(modal_name),
                                                        escape(modal_name), escape(modal_name)))

        output.append(
            ' <button id="filter{}"  class="btn btn-primary btn-full-width"  name="search"> Search </button> '.format(
                escape(name)))
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        userentry = request.user
        entry = UserSettings.objects.filter(user_link=userentry).first()

        self.fields = str(getattr(entry, str(self.model) + str("_list_activefields"))).replace("[", "").replace("]",
                                                                                                                "").replace(
            "'", "").replace(" ", "").split(",")
        for field in self.fields:
            output.append(
                " <div class='col-sm'> <label >{}</label> <input type='text' id='{}'> </div>".format(
                    field.split('__')[0], field.split('__')[0]))

        output.append('''
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                Search Results
                            </h4>
                        </div>
                            <div class="panel-body">
                                <div class="col-sm-12" id='results_wrapped'>
                                    <table id="results{}" class="table table-striped table-bordered"> </table>
                                </div>
                            </div>
                    </div>'''.format(escape(name)))
        output.append('''</div> <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" id="{}" class="btn btn-primary">Add selected rows</button>
                       </div></div> </div> </div>'''.format(escape(modal_add_button)))
        output.append(
            "<script>$('.openmodal{}').click(function(){{ $('#{}').modal('show'); document.getElementById('filter{}').click();}});var table;</script>".format(
                escape(modal_name), escape(modal_name), escape(name), escape(name)))

        output.append(" <script>  $('#filter{}').click(function(e) ".format(escape(name)))
        output.append(''' {{ e.preventDefault();
	     var content={{}};
		$("#{}widget input").each(function(e)
		{{	
		var key = this.id;
        if (typeof key === "undefined") {{
            return
        }}

        //avoid empty shadowed parameters
         if(this.value != ''){{
            content[key] = this.value;
         }}
		}});
	 //avoid empty shadowed parameters
         if(this.value != ''){{
            content[key] = this.value;
         }}
	content['csrfmiddlewaretoken'] = getCookie('csrftoken');
	content['widget'] = "nestedwidget";
	    //content['modelname'] = '{}';

        '''.format(escape(name), escape(name)))
        output.append(' table = $("#results{}").DataTable( '.format(escape(name)))
        output.append('''		
		{
                "searching": false,
                "paging": true,
                "pageLength": 25,
                "serverSide": true,
                "order": [[0, "asc"]],
				"select": 'single',
                "destroy": true,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
			    "ajax": {
		''')
        output.append(' "url": "" ,')
        output.append('''
                    "data": content,
                    "type": "POST",

                },
                columns: [	''')

        for column in self.fields:
            output.append("	{{data: '{}' , 'title': '{}'}},".format(column, column))
        output.append('''			
                ],

            });
			table.on('select.dt', function() {
			  var array = [];
			  table.rows('.selected').every(function(rowIdx) {
				 array.push(table.row(rowIdx).data())
			  })   

			})
        })


</script>
             ''')
        output.append("""<script>
						$('#{}').click(function()
							{{ 
				table.rows('.selected').every(function(rowIdx) {{
					 value =  table.row(rowIdx).data()['id'].toString()
					 """.format(modal_add_button))

        if (self.model in selectdict):
            output.append("""text = """)
            firstitem = False
            for item in selectdict[self.model]['list']:
                if (firstitem == True):
                    output.append('''+''')
                output.append(''' table.row(rowIdx).data()["''' + item + '''"]''')
                firstitem = True

        output.append("""
					 var selectoptions = []
				Array.from(document.querySelector(".{}").options).forEach(function(option_element) {{
					let option_text = option_element.text;
					let option_value = option_element.value;
					selectoptions.push(option_value)
				}});
				function contains(arr, element) {{
					for (var i = 0; i < arr.length; i++) {{
						if (arr[i] === element) {{
							return true;
						}}
					}}
					return false;
				}}

			   if (contains(selectoptions, value))
			   {{
			 $("#id_{}").val(value).trigger('change');

			   }}
			   else
			   {{
			   var newOption = new Option(text, value, true, true);
				$("#id_{}").append(newOption).trigger('change');
			   }}   			
					}});		

				table.clear().destroy();
			    $(".modal").modal("hide");
				}})
				 </script>""".format(escape(name), escape(name), escape(name), escape(name), escape(name), escape(name),
                                     escape(name),
                                     modal_name))

        output.append("</div>")

        return mark_safe('\n'.join(output))


class multiselectfilterwidget(SelectMultiple):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """

    def __init__(
            self,
            fields,
            filter,
            selectname,
            model,
            *args,
            **kwargs
    ):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(multiselectfilterwidget, self).__init__(*args, **kwargs)
        self.fields = fields
        self.filter = filter
        self.selectname = selectname
        self.model = model

    def render(self, name, value,
               attrs=None, choices=(), *args, **kwargs):
        if value is None:
            value = []
        if isinstance(self.choices, list):
            choices = self.choices
        else:
            choices = []

        output = []
        modal_name = 'modal' + escape(name)
        modal_add_button = 'modal_add_button_' + escape(name)
        output.append('<div class = "row"><div class = "col-10><div id="{}widget">'.format(escape(name)))
        output.append(
            '''

<select name="{}" id="id_{}"  class="{}"  multiple="multiple" style="width:75%"></select></div><div class = "col-2> <button type="button" class="btn btn-info btn-lg openmodal{}" data-toggle="modal"  data-target="#{}"><i class="fas fa-link"></i></button></div></div> 
			<!-- Modal -->
            <div class="modal fade" id="{}" tabindex="-1" role="dialog" aria-hidden="false">
                <div class="modal-dialog modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="false">&times;</span>
                            </button>
                        </div>
                    <div class="modal-body" >'''.format(escape(name), escape(name), escape(name), escape(modal_name),
                                                        escape(modal_name), escape(modal_name)))

        output.append(
            ' <button id="filter{}"  class="btn btn-primary btn-full-width"  name="search"> Search </button> '.format(
                escape(name)))

        for field in self.filter:
            output.append(
                " <div class='col-sm'> <label >{}</label> <input type='text' id='{}'> </div>".format(
                    field.split('__')[0], field.split('__')[0]))

        output.append('''
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                Search Results
                            </h4>
                        </div>
                            <div class="panel-body">
                                <div class="col-sm-12" id='results_wrapped'>
                                    <table id="results{}" class="table table-striped table-bordered"> </table>
                                </div>
                            </div>
                    </div>'''.format(escape(name)))
        output.append('''</div> <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" id="{}" class="btn btn-primary">Add selected rows</button>
                       </div></div> </div> </div>'''.format(escape(modal_add_button)))

        output.append(
            "<script>$('.openmodal{}').click(function(){{ $('#{}').modal('show');document.getElementById('filter{}').click();}});  var table;</script>".format(
                escape(modal_name), escape(modal_name), escape(name)))
        output.append(" <script>  $('#filter{}').click(function(e) ".format(escape(name)))
        output.append(''' {{ e.preventDefault();
	    var content={{}};
		$("#{}widget input").each(function(e)
		{{	
		var key = this.id;
        if (typeof key === "undefined") {{
            return
        }}
         //avoid empty shadowed parameters
         if(this.value != ''){{
            content[key] = this.value;
         }}

		}});

		content['csrfmiddlewaretoken'] = getCookie('csrftoken');
	    //content['modelname'] = '{}';
		console.log(content)
        '''.format(escape(name), escape(name)))
        output.append(' table = $("#results{}").DataTable( '.format(escape(name)))
        output.append('''		
		{
                "searching": false,
                "paging": true,
                "pageLength": 25,
                "serverSide": true,
                "order": [[0, "asc"]],
                "destroy": true,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
				 select: {
					style: "multi"
				},
                "ajax": {
		''')
        output.append(' "url": "" ,')
        output.append('''
        		"data": content,
                    "type": "POST"
                },
                   columns: [	''')
        for column in self.fields:
            output.append("	{{data: '{}' , 'title': '{}'}},".format(column, column))
        output.append('''			
                ],
            });
        })
</script>
             ''')
        output.append("""<script>
						$('#{}').click(function()
							{{ 
				table.rows('.selected').every(function(rowIdx) {{
					 value =  table.row(rowIdx).data()['id'].toString()
					 text = table.row(rowIdx).data()["{}"]
					 var selectoptions = []
Array.from(document.querySelector(".{}").options).forEach(function(option_element) {{
    let option_text = option_element.text;
    let option_value = option_element.value;
    selectoptions.push(option_value)
}});
function contains(arr, element) {{
    for (var i = 0; i < arr.length; i++) {{
        if (arr[i] === element) {{
            return true;
        }}
    }}
    return false;
}}

			   if (contains(selectoptions, value))
			   {{
			   previouselm = []
			   Array.from(document.querySelector(".{}").options).forEach(function(option_element) {{
    let option_text = option_element.text;
    let option_value = option_element.value;
	let is_option_selected = option_element.selected;
	if (is_option_selected === true)
	{{previouselm.push(option_value)}}
		}});
           previouselm.push(value)
		   $(".{}").val(previouselm).trigger('change')


			   }}
			   else
			   {{
			   var newOption = new Option(text, value, true, true);
				$(".{}").append(newOption).trigger('change');
			   }}   			
					}});					   
				table.clear().destroy();
			    $("#{}").modal("hide");
				}})
				 </script>""".format(modal_add_button, self.selectname, escape(name), escape(name), escape(name),
                                     escape(name), modal_name))
        output.append('''<script>

					var xo = {};

					xo.forEach((obj, i) => {{

					var newOption = new Option(obj.value, obj.id, true, true);
					$('.{}').append(newOption).trigger('change');
									}});

								</script>'''.format(escape(name), choices, escape(name)))
        output.append("</div>")
        return mark_safe('\n'.join(output))


def get_underscore_attrs(attrs, item):
    for attr in attrs.split('__'):
        if callable(attr):
            item = attr(item)
        elif callable(getattr(item, attr)):
            item = getattr(item, attr)
        else:
            item = getattr(item, attr)
    if item is None:
        return ""
    return item


def clean_underscores(string):
    """
    Helper function to clean up table headers.  Replaces underscores
    with spaces and capitalizes words.
    """
    s = capwords(string.replace("_", " "))
    return s


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", _("Keine Auswahl")), ("true", _("Yes")), ("false", _("No")))


class datetimepickerfield(forms.DateTimeInput):
    def __init__(self, *args, **kwargs):
        super(datetimepickerfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group"><div class="controls">'''
        attrs.update({'class': "form-control datetimepicker"})
        attrs.update({'style': "border-radius: 4px;"})
        html += super(datetimepickerfield, self).render(name, value, attrs)

        html += '''                    
                        </div>
                    </div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class fileuploadfield(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super(fileuploadfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        attrs.update({'style': "border-radius: 4px;", 'multiple': True})
        html = '</br>' + super(fileuploadfield, self).render(name, value, attrs) % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        html += '''<output id="list"></output>'''
        return mark_safe(html)


class timepickerfield(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        super(timepickerfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group"><div class="controls">'''
        attrs.update({'class': "form-control timepicker"})
        attrs.update({'style': "border-radius: 4px;"})
        html += super(timepickerfield, self).render(name, value, attrs)

        html += '''                    
                        </div>
                    </div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class treemultipleselectfield(forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        self.node = kwargs.pop('node', None)

        super(treemultipleselectfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">
                        <div class="controls">

                        '''
        attrs.update({'multiple': "multiple"})

        attrs.update({'class': "treeview"})
        attrs.update({'style': "width: 100%"})

        html += ''' <div class="col-lg-6">
			<h3>Single Selection</h3>
			<input type="text" id="justAnotherInputBox" placeholder="Type to filter" autocomplete="off"/>
		</div>            </div></div><script>def jsondata = ''' + self.node + '''</script>

    ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class multiselectfield(forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        super(multiselectfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">
                        <div class="controls">

                        '''
        attrs.update({'multiple': "multiple"})

        attrs.update({'class': "form-control select2"})

        html += super(multiselectfield, self).render(name, value, attrs)
        html += '''             </div></div>

    ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class selectfield(forms.Select):

    def __init__(self, *args, **kwargs):
        super(selectfield, self).__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):

        if 'class' in base_attrs:
            string = "form-control " + str(base_attrs['class'])

            dict = {'class': string}
        else:
            dict = {'class': "form-control"}
        extra_attrs.update(dict)

        return super().build_attrs(base_attrs, extra_attrs=extra_attrs)


class checkbox(forms.CheckboxInput):

    def __init__(self, *args, **kwargs):
        super(checkbox, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">


                            '''
        attrs.update({'style': "border-radius: 4px;"})
        html += super(checkbox, self).render(name, value, attrs)

        html += '''


                    </div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class integerfeld(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        super(integerfeld, self).__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        if 'class' in base_attrs:
            string = "form-control " + str(base_attrs['class'])

            dict = {'class': string}
        else:
            dict = {'class': "form-control"}
        extra_attrs.update(dict)
        return super().build_attrs(base_attrs, extra_attrs=extra_attrs)


class decimalfeld(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        super(decimalfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
                        <div class="form-group">


                            '''

        html += '''</span>
                            <div class="controls">'''
        attrs.update({'class': "form-control"})
        attrs.update({'placeholder': name.title()})
        attrs.update({'style': "border-radius: 4px;"})
        html += super(decimalfeld, self).render(name, value, attrs)

        html += '''                    </div>

                    </div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class textinputfeld(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super(textinputfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">


                                            <div class="controls">'''
        if 'class' in final_attrs:
            classes = "form-control " + str(final_attrs['class'])
        else:
            classes = "form-control "

        attrs.update({'class': classes})

        if ('disabled' in final_attrs):
            attrs.update({'disabled': 'disabled'})
        attrs.update({'class': "form-control"})
        html += super(textinputfeld, self).render(name, value, attrs)

        html += '''                    
                        </div></div>
                    ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class emailfield(forms.EmailInput):
    def __init__(self, *args, **kwargs):
        super(emailfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):

        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">


                                                <div class="controls">'''
        attrs.update({'class': "form-control selectize_email"})

        attrs.update({'style': "border-radius: 4px;"})
        html += super(emailfield, self).render(name, value, attrs)

        html += '''                    
                            </div></div>
                        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class passwordfeld(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        super(passwordfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)

        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">
                                            <!-- <label class="form-label" for="field-6">''' + name.title() + '''</label> -->

                                            <div class="controls">'''
        attrs.update({'class': "form-control textarea"})
        attrs.update({'cols': "5"})

        attrs.update({'placeholder': 'Passwort eingeben'})
        attrs.update({'style': "border-radius: 4px;"})
        html += super(passwordfeld, self).render(name, value, attrs)

        html += '''<span toggle="#''' + attrs['id'] + '''" class="fa fa-fw fa-eye field-icon toggle-password">                    

                    </div></div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class textarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(textarea, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">
                    '''
        attrs.update({'class': "form-control", 'rows': "7"})
        html += super(textarea, self).render(name, value, attrs)

        html += '''</div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class textarea_urllink(forms.TextInput):
    def __init__(self, url, *args, **kwargs):
        super(textarea_urllink, self).__init__(*args, **kwargs)
        self.url = url

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)
        html = '''<div class="row"><div class="col-11">
        <div class="controls">'''
        attrs.update({'class': "form-control textarea"})
        attrs.update({'cols': "5"})

        attrs.update({'style': "border-radius: 4px;"})
        html += super(textarea_urllink, self).render(name, value, attrs)

        html += '''                    

                    </div></div><div class="1"><a href="''' + str(
            self.url) + '''" ><i class="fas fa-link"></i></a></div></div>''' % {
                    'attrs': flat_attrs,
                    'id': attrs['id'],
                    'value': value,
                }
        return mark_safe(html)


class datepickerfield(forms.DateInput):
    def __init__(self, *args, **kwargs):
        super(datepickerfield, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div class="form-group">


                                            <div class="controls">'''

        attrs.update({'data - date - format': "dd.mm.yyyy"})
        attrs.update({'class': "form-control datepicker"})
        attrs.update({'autocomplete': "off"})
        attrs.update({'placeholder': 'dd.MM.yyyy'})
        attrs.update({'style': "border-radius: 4px;"})
        html += super(datepickerfield, self).render(name, value, attrs)

        html += '''                    
                        </div>
                    </div>''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


# Alt -------------------------------------------------------------------------------------------------------------------


class zeitfeld(forms.DateInput):

    def __init__(self, *args, **kwargs):
        super(zeitfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)

        flat_attrs = flatatt(attrs)

        html = '''<div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''

        html += ''' 
            <div class="form-group">
                <div class="input-icon right">
                <i class="fa fa-calendar"></i>'''
        attrs.update({'width': "100%"})
        attrs.update({'style': " "})
        attrs.update({'autocomplete': "off"})
        html += super(zeitfeld, self).render(name, value, attrs)
        html += '''


        </div>
            </div>


        </div>


        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class checkbox2(forms.CheckboxInput):
    class Media:
        css = {
            'all': ('/home/sebastian/PycharmProjects/tanzpartner/static/tanzpartner/css/checkbox.css',),

        }

    def __init__(self, *args, **kwargs):
        super(checkbox, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<style>
                    #Formular input {
    float: left;

    margin-left: 0px;



}
                    </style>'''
        html += '''<div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''

        html += ''' <h5>
            <div class="form-group">
            <div class="input-icon right">'''
        attrs.update({'width': "100%"})
        attrs.update({'style': " "})
        html += super(checkbox, self).render(name, value, attrs)

        html += '''  </div></div>
            </div>

        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class textarea2(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(textarea, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
        <style>
            input {
                width: 100%;
            }
        </style>
        <div style="margin-left: 20px; margin-bottom: 20px; width:20%; float:left;">

            <h5>''' + final_attrs['placeholder'] + '''</h5>
            <table width="100%">
                <tr>
                    <td>

            '''
        html += super(textarea, self).render(name, value, attrs)

        html += '''
                    </td>
                    </tr>
                    <tr><td></td></tr>
                    </table>

                </div>
                ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,

            # 'class': final_attrs['class']
        }
        return mark_safe(html)


class datumsfeld(forms.DateInput):

    def __init__(self, *args, **kwargs):

        super(datumsfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if (value == None):
            value = datetime.now().strftime("%d.%m.%Y")
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''<div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''

        html += ''' <h5>
            <div class="form-group">
                <div class="input-icon right">
                <i class="fa fa-calendar"></i>'''

        attrs.update({'width': "100%"})
        attrs.update({'style': ""})
        attrs.update({'autocomplete': "off"})
        attrs.update({'type': "datum"})

        html += super(datumsfeld, self).render(name, value, attrs)
        html += '''


        </div>
            </div>


        </div>


        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class dezimalfeld(forms.NumberInput):

    def __init__(self, *args, **kwargs):
        super(dezimalfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
        <div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''

        html += '''    <h5>''' + final_attrs['placeholder'] + '''</h5>
            <div class="form-group">

                '''

        attrs.update({'width': "100%"})
        attrs.update({'style': ""})
        html += super(dezimalfeld, self).render(name, value, attrs)
        html += '''

            </div>

        </div>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class integerfeld2(forms.NumberInput):

    def __init__(self, *args, **kwargs):

        super(integerfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
        <div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''

        html += '''    <h5></h5>
            <div class="form-group">

                '''

        attrs.update({'width': "100%"})
        attrs.update({'style': ""})
        html += super(integerfeld, self).render(name, value, attrs)
        html += '''

            </div>

        </div>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
        }
        return mark_safe(html)


class textfeld(forms.TextInput):
    def __init__(self, *args, **kwargs):

        super(textfeld, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
        <style>
            input {
                width: 100%;
            }
        </style>
        <div style="margin-left: 20px; margin-bottom: 20px; float:left;'''
        if ('style' in final_attrs):

            html += str(final_attrs['style']) + '''">'''
        else:
            html += '''width:20%;">'''
        if ('placeholder' in final_attrs):
            html += '''<h5>''' + final_attrs['placeholder'] + '''</h5>'''

        html += '''<table width="100%">
                <tr>
                    <td>

            '''
        attrs.update({'width': "100%"})
        attrs.update({'style': ""})
        html += super(textfeld, self).render(name, value, attrs)

        html += '''
            </td>
            </tr>
            <tr><td></td></tr>
            </table>

        </div>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,

            # 'class': final_attrs['class']
        }
        return mark_safe(html)


