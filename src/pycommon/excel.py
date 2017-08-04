import xlrd
import xlwt


##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对excel操作的简单封装，方便操作excel时调用</p>
# <br/><br/>
# <p>该文件引用了xlrd,xlwt库作来操作excel</p>
# <p>主要包含了读取excel(read_xls)和写入excel(write_xls)，具体使用方法看参数说明</p>
#
##

def read_xls(file_path, has_header=True, dict_data=False, sheet_name=0):
    """
        读取excel，返回的结果为{headers:[],data:[]}
        当前只支持单个sheet book的
    :param file_path: 文件路基
    :param has_header: 是否有文件头，如果为Ture则第一行当文件头
    :param dict_data: 是否以数字的方式显示
    :param sheet_name:
    :return:
    """

    xls_workbook = xlrd.open_workbook(file_path)
    table = xls_workbook.sheets()[sheet_name]
    header = []
    data = []
    data_index = 0
    col_names = []

    if has_header:
        data_index = 1
        header = table.row_values(0)
    if dict_data is True:
        for item in header:
            col_name = item
            index = 1
            while col_name in col_names:
                col_name = "{0}{1}".format(item, index)
                index = index + 1
            col_names.append(col_name)
    # print(col_names)
    for row_index in range(data_index, table.nrows):
        if dict_data is False:
            data.append(table.row_values(row_index))
        else:
            data_item = {}
            for col_index in range(0, table.ncols):
                data_item[col_names[col_index]] = table.cell(row_index, col_index).value
            data.append(data_item)
    return {'header': header, "data": data}


def write_xls(file_path, datas=[], headers=[]):
    """
        把数据写入到xls，当前只支付单个工作薄的写入
    :param file_path: excel保存路基
    :param datas: 保存数据
    :param headers: 保存头
    :return:
    """
    xls_file = xlwt.Workbook()
    table = xls_file.add_sheet('Sheet1', cell_overwrite_ok=True)
    row_index = 0;
    if headers is not None and len(headers) > 0:
        for index in range(0, len(headers)):
            table.write(0, index, headers[index])
        row_index = 1
    for data_index in range(0, len(datas)):
        # 索引篇历
        x_row_index = row_index + data_index
        data_item = datas[data_index]
        if isinstance(data_item, dict):
            for col_index in range(0, len(headers)):
                key = headers[col_index]
                if data_item.get(key) is not None:
                    table.write(x_row_index, col_index, data_item[key])
        else:
            for col_index in range(0, len(data_item)):
                table.write(x_row_index, col_index, data_item[col_index])
    xls_file.save(file_path)


if __name__ == "__main__":
    # arr =['用户名', '年龄', '呵呵', '用户名']
    # print('用户名' in arr)
    # print(read_xls(r"E:\Works\test\xlrdtest.xlsx",True,True))
    write_xls(r"abc123.xls", datas=[[1, 2, 3, 4], [2, 4, 6, 8], [7, 8, 9, 10], ],
              headers=['用户名', '年龄', '呵呵', '用户名1'])
