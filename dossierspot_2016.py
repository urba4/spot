import arcpy
import os
import shutil
import win32com.client as win32

    
def get_depcoms(depcoms_path):
    '''read depcoms file : return qry str'''
    with open(depcoms_path) as f:
        
        depcoms_lst = [line.rstrip(u'\n') for line in f.readlines()]
        depcoms_str = '\'' + '\', \''.join(depcoms_lst) + '\''

    return depcoms_lst, depcoms_str


def build_subfolders(root_folder):
    '''will build subfolders'''

    for folder in [ur'xlsx', ur'lyr', ur'mxd', ur'pdf\pages']:
        
        new_folder = os.path.join(root_folder, folder)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

   
def get_pathes(pagesize=None):
    '''builds all pathes (templates, files, pdfs)
    returns io list of tuples'''

    io = []

    # mxds
    for tpl in mxd_tpl:
        i = os.path.join(tpl_root, tpl)
        o = os.path.join(root_folder, 'mxd', tpl.replace('tpl', naming))
        pdf = os.path.join(
            root_folder, 'pdf', 'pages',
            os.path.splitext(tpl)[0].replace('tpl', naming) + '.pdf')
        io.append((i, o, pdf))

    # xlsx
    i = os.path.join(tpl_root, xlsx_tpl)
    o = os.path.join(root_folder, 'xlsx', xlsx_tpl.replace('tpl', naming))
    pdf = os.path.join(
        root_folder, 'pdf', 'pages',
        os.path.splitext(xlsx_tpl)[0].replace('tpl', naming) + '.pdf')
    io.append((i, o, pdf))

    return io


def process_file(file_path, pdf_path):
    '''switch between file types'''

    filetype = os.path.basename(file_path).split('_')[0]
    
    {'st':      tune_st,                                    # millesime maps
     'evo':     tune_evo,                                   # evo maps
     'ortho':   tune_ortho,                                 # ortho maps
     'data':    tune_data}[filetype](file_path, pdf_path)   # xlsx files
    
def tune_st(st, pdf):
    '''will tune st mxd
        mxd : path to mxd'''

    # copy and get get mxd, set export pathes
    lyr = os.path.join(
        root_folder,
        'lyr',
        os.path.splitext(os.path.basename(st))[0]) + '.lyr'
        
    mxd = arcpy.mapping.MapDocument(st)

    #   - set title
    mxd.title = naming

    #   - set spot layer definition query
    styr_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name.split()[0] == 'spot'][0]
        
    styr_lyr.definitionQuery = u'depcom_2015 in ({})'.format(depcoms_str)

    #   - set mapper zoom
    styr_extent = styr_lyr.getExtent()
    mapper = [
        df for df in arcpy.mapping.ListDataFrames(mxd)
        if df.name == 'carte'][0]
        
    mapper.extent = styr_extent
    mapper.scale = mapper.scale * 1.1

    #   - set cartogram definition queries
    perimfill_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_fill'][0]
        
    perimborder_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_border'][0]

    perimfill_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)
    
    perimborder_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)

    #   - save, export pdf and del
    mxd.save()
    styr_lyr.saveACopy(lyr)
    arcpy.mapping.ExportToPDF(mxd, pdf)

    del mxd


def tune_evo(evo, pdf):
    '''will tune evo mxd
        mxd : path to mxd'''

    # get mxd, yro, yre, set pdf path
    yro, yre = os.path.basename(evo).split('_')[1:-1]
    mxd = arcpy.mapping.MapDocument(evo)

    #   - set title
    mxd.title = naming

    #   - set mapper definition queries
    evo_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name.split()[0] == 'Evolution'][0]
    
    styro_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name.split()[0] == 'Occupation'][0]

    evo_lyr.definitionQuery = (
        u'(ST_{yro} > 50 and ST_{yro} <> 90) '
        u'and (ST_{yre} = 90 or ST_{yre} <  50) '
        u'and depcom_2015 in ({depcoms})').format(
        depcoms=depcoms_str , yro=yro, yre=yre)
    
    styro_lyr.definitionQuery = u'depcom_2015 in ({})'.format(depcoms_str)

    #   - set mapper zoom
    styro_extent = styro_lyr.getExtent()
    mapper = [
        df for df in arcpy.mapping.ListDataFrames(mxd)
        if df.name == 'carte'][0]
        
    mapper.extent = styro_extent
    mapper.scale = mapper.scale * 1.1

    #   - set cartogram definition queries
    perimfill_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_fill'][0]
        
    perimborder_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_border'][0]
        
    perimfill_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)
    perimborder_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)

    #   - save and del
    mxd.save()
    arcpy.mapping.ExportToPDF(mxd, pdf)

    del mxd


def tune_ortho(ortho, pdf):
    '''will tune ortho mxd
        mxd : path to mxd'''

    # get mxd, set pdf path
    mxd = arcpy.mapping.MapDocument(ortho)

    #   - set title
    mxd.title = naming

    #   - set mapper definition query
    orthozoom_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'zoom'][0]
    
    orthomask_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'mask'][0]
    
    orthozoom_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)
    
    orthomask_lyr.definitionQuery = (
        u'not CODE_INSEE like \'6938%\' '
        u'and not CODE_INSEE in ({})').format(depcoms_str)

    #   - set mapper zoom
    zoom_extent = orthozoom_lyr.getExtent()
    
    mapper = [
        df for df in arcpy.mapping.ListDataFrames(mxd)
        if df.name == 'carte'][0]
    
    mapper.extent = zoom_extent
    mapper.scale = mapper.scale * 1.1

    #   - set cartogram definition queries
    perimfill_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_fill'][0]
    perimborder_lyr = [
        lyr for lyr in arcpy.mapping.ListLayers(mxd)
        if lyr.name == 'perim_border'][0]
    
    perimfill_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)
    perimborder_lyr.definitionQuery = u'CODE_INSEE in ({})'.format(depcoms_str)

    #   - save, export pdf and del
    mxd.save()
    arcpy.mapping.ExportToPDF(mxd, pdf)
    
    del mxd


def tune_data(xlsx, pdf):
    '''will tune xlsx
        xlsx : path to xlsx'''

    # extract data from lyr file
    flds = [
        'depcom_2015',
        'ST_00', 'ST_05', 'ST_10', 'ST_15',
        'ST5_05', 'ST5_10', 'ST5_15',
        'SHAPE@AREA']
    
    # /!\ FeatureClassToNumPyArray can't handle <null> /!\
    data = arcpy.da.FeatureClassToNumPyArray(
        fc, flds, u'depcom_2015 in ({})'.format(depcoms_str))

    #   - insert data in template xlsx
    excel = win32.gencache.EnsureDispatch('Excel.Application')

    wb = excel.Workbooks.Open(xlsx)

    ws_data = wb.Worksheets('data')
    ws_data.Range('A2:I'+str(data.size+1)).Value = data
    ws_data.Range('J2:W2').AutoFill(
        Destination=ws_data.Range('J2:W'+str(data.size+1)))

    #   - update titles
    ws_titles = wb.Worksheets('titres')
    ws_titles.Range('A2').Value = naming

    #   - update all pivot tables
    for sh in wb.Worksheets:
        for pt in sh.PivotTables():
            pt.RefreshTable()

    #   - export pdf and close xlsx (no save required)
    wb.ExportAsFixedFormat(
        From=1, To=12, Type=0, Filename=pdf, IgnorePrintAreas=False)

    wb.Close(True)


def assemble_pdf(io):
    '''will assemble all pdf pages in one doc'''

    # list pdf pages
    inputs = [item[2] for item in io]
    
    # build final pdf path
    output = os.path.join(
        root_folder, 'pdf', u'{name}.pdf'.format(name=naming))
        
    # create pdf doc via arcpy
    pdfDoc = arcpy.mapping.PDFDocumentCreate(output)

    # append pages
    for i in inputs:
        pdfDoc.appendPages(i)

    # save and close
    pdfDoc.saveAndClose()

    # delete object
    del pdfDoc

if __name__ == "__main__":

    # consts
    #   - spot datasource (in case)
    fc = ur'J:\Etudes\laufma\thema\methode 2015\20160113_expertise_source_ftp\analyse.gdb\topo\st_draft'

    #   - mxd and xlsx templates
    tpl_root = ur'J:\Etudes\laufma\Python26\site-packages\mezcal\templates\2016'

    mxd_tpl = [
        ur'st_00_tpl.mxd',
        ur'st_05_tpl.mxd',
        ur'st_10_tpl.mxd',
        ur'st_15_tpl.mxd',
        ur'evo_00_10_tpl.mxd',
        ur'evo_05_15_tpl.mxd',
        ur'evo_00_15_tpl.mxd',
        ur'evo_00_05_tpl.mxd',
        ur'evo_05_10_tpl.mxd',
        ur'evo_10_15_tpl.mxd',
        ur'ortho_05_tpl.mxd',
        ur'ortho_16_tpl.mxd']

    xlsx_tpl = ur'data_tpl.xlsx'

    #   - get parameter values
    root_folder = os.path.dirname(arcpy.GetParameterAsText(0))
    naming = os.path.basename(root_folder)
    depcoms_lst, depcoms_str = get_depcoms(arcpy.GetParameterAsText(0))

    # query strings
    #   - generic millesime query string
    qry_styr = u'depcom_2015 in ({depcoms})'

    #   - generic mask query string
    qry_mask = (
        u'not CODE_INSEE like \'6938%\' '
        u'and not CODE_INSEE in ({depcoms})')

    #   - generic evo query string
    qry_evo = (
        u'(ST_{yro} > 50 and ST_{yro} <> 90) '
        u'and (ST_{yre} = 90 or ST_{yre} <  50) '
        u'and depcom_2015 in ({depcoms})')

    # build subfolders
    build_subfolders(root_folder)

    # get all pathes
    io = get_pathes()

    # process !!!
    for i, o, pdf in io:
        shutil.copy(i, o)       # copy template to path
        process_file(o, pdf)    # tune file by type (switch)
        
    # assemble final pdf
    assemble_pdf(io)
