nest-css
========

Script to nest all rules of a CSS document inside an arbitrary selector.

Example
-------

Running:

.. code-block:: shell

 ./nest-css.py original.css '#container' > modified.css

on ``original.css``:

.. code-block:: css

 @namespace "http://www.w3.org/1999/xhtml";
 
 /* children of the <head> element all have display:none */
 head, link, meta,
 script, style, title {
     display: none;
 }
 
 body {
     display: block;
     margin: 8px;
 }

 input, input:matches([type="password"], [type="search"]) {
     border-radius: 5px;
     border: 1px solid #4c4c4c;
     cursor: auto;
 }

would give ``modified.css``:

.. code-block:: css

 @namespace "http://www.w3.org/1999/xhtml";

 /* children of the <head> element all have display:none */
 #container head, #container  link, #container  meta,
 #container  script, #container  style, #container  title {
     display: none;
 }
 
 #container body {
     display: block;
     margin: 8px;
 }

 #container input, #container input:matches([type="password"], [type="search"]) {
     border-radius: 5px;
     border: 1px solid #4c4c4c;
     cursor: auto;
 }
