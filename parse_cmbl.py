## see https://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python
## also https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
## note some cmbl files seem to be "binary" in which case they are just gzipped.

from xml.dom import minidom
from datetime import datetime
import pandas as pd

##xmldoc = minidom.parse('isb-2/CLAUDIA-Benchfiles-Laptop/Aquaponics Bench test 2014/lab bench run 1.cmbl')
xmldoc = minidom.parse('lab bench run 7.cmbl')

#itemlist = xmldoc.getElementsByTagName('DataObjectName') 
#print itemlist[0].childNodes[0].nodeValue

itemlist = xmldoc.getElementsByTagName('DataColumn')
df_data = pd.DataFrame()
df_metadata = None
for i in range(len(itemlist)):
    name = itemlist[i].getElementsByTagName('DataObjectName')[0].childNodes[0].nodeValue
    short_name = itemlist[i].getElementsByTagName('DataObjectShortName')[0].childNodes[0].nodeValue
    try: ## for pH, itemlist[i].getElementsByTagName('ColumnUnits')[0].childNodes is an empty list
        units = itemlist[i].getElementsByTagName('ColumnUnits')[0].childNodes[0].nodeValue
    except:
        units = ''
    startTime = itemlist[i].getElementsByTagName('StartTime')[0].childNodes[0].nodeValue
    startCollectTime = itemlist[i].getElementsByTagName('ColumnStartCollectTime')[0].childNodes[0].nodeValue
    data = str(itemlist[i].getElementsByTagName('ColumnCells')[0].childNodes[0].nodeValue).split('\n')
    print name, short_name, units, startTime, startCollectTime, len(data)
    data = pd.np.array( data )
    data = data[ data != '' ]
    data = data.astype( pd.np.float )
    tmp_df = pd.DataFrame( {'name':name, 'shortName':short_name, 'units':units, 'length':len(data)}, index=[i] )
    if df_metadata is None:
        df_metadata = tmp_df
    else:
        df_metadata = df_metadata.append( tmp_df )
    if name == 'Time':
        data = data + float(startTime)
    df_data[ name ] = pd.Series(data)
    if name == 'Time':
        ts = [datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S') for t in data]
    df_data[ 'TimeString' ] = pd.Series(ts)
    #print ''

writer = pd.ExcelWriter('lab bench run 7.xlsx')
df_metadata.to_excel( writer, 'MetaData' )
df_data.to_excel( writer, 'Data' )
writer.save()

