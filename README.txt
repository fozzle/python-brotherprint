===================
BrotherPrint
===================

Brother networked label printers library for Python

Supported models:
* QL-580N


Usage
=====

This library supports two printing modes. ESC/P commands, and templates. I highly recommend using templates, because it is easier to manage, and offers more features. I will, however, go over both.
You should review the official Brother documentation `here (ESCP Docs)<http://www.mediafire.com/?3wbanr34bsr18dw>`_ and `here (Template Command Docs)<http://www.mediafire.com/?v798mue7i58ed66>`_, to know what is available.

Setup
=====

Regardless of which mode you are using, you need to intialize and connect a socket object, and pass the resulting socket object to the BrotherLabel object instantiator.
    f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f_socket.connect((<ip_address>,<port (9100 by default for QL580N)>))
    printjob = BrotherPrint(f_socket)

ESC/P Printing
--------------
Invoke escp commands through certain BrotherLabel object methods (see actual file for method descriptions)
Make sure to end with a form feed, signifying the end of a label.
    printjob.command_mode()
    printjob.bold('on')
    printjob.send(<text>)
    printjob.print_page(<cut_setting>)

Template Printing
-----------------
Create your template and upload it to the printer. After creating a BrotherLabel object, call template_mode() to set the printer to template mode, and then use the template commands to fill in your label.

    printjob.template_mode()
    printjob.template_init()
    printjob.choose_template(<template_number>)
    printjob.select_and_insert(<field_name>, <data>)
    printjob.select_and_insert(<field_name2>, <data2>)
    printjob.select_and_insert(<field_name3>, <data3>)
    printjob.template_print()

