python-brotherprint
===================

Brother QL-580N networked printers library for Python

* TODO: Need to make this into a proper Python library.
* TODO: Update documentation, provide examples.


Usage
=====

This library supports two printing modes. ESC/P commands, and templates. I highly recommend using templates, because it is easier to manage, and offers more features. I will, however, go over both.

## Setup
Regardless of which mode you are using, you need to intialize a socket connection, and pass the resulting socket object to the BrotherLabel object instantiator.

### ESC/P Printing
Invoke escp commands through certain BrotherLabel object methods (see actual file for method descriptions)
Make sure to end with a form feed, signifying the end of a label.

### Template Printing
Create your template and upload it to the printer. After creating a BrotherLabel object, call template_mode() to set the printer to template mode, and then use the template commands to fill in your label.


