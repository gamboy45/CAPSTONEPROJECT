SimpleFlaskApp
==============

A skeletal Flask application with Bootstrap 3.x based UI

Dependencies
==============


| Python modules: |
| ------ |
| flask |
| flask_sql_alchemy |
| flask_table
| MySQLdb |
| pytz |


Basic Layout
============



/
   appconfig.py
   run.py

   flaskapp/

       CONFIG.py
       context.py
       models.py
       routes.py
       trace.py

       static/
          css/
             style.css
             packt_style.css
          img/
             favicon.ico
          js/
             demo.js

       templates/
           _errors/
              404.html
              500.html
           _layouts/
              basic.html
              calendar.html
              cal_datatable.html
              datatable.html
              fullcalendar.html
           _view/
           _edit/
           _new/
           _parts/
              nav_menu.html
           _modal/
              search.html

