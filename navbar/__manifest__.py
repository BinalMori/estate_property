{
    'name': "Navbar",
    'author':'binal',
    "sequence":-80,
    "application":True,
    "depends": ["web"],
    "assets": {
       'web.assets_backend': [
           '/navbar/static/src/js/navbar.js',
       ],
       'web.assets_qweb': [
           '/navbar/static/src/xml/navbar_template.xml',
       ],
    },

}
