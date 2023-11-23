/* eslint-disable */
require('script-loader!file-saver');
require('script-loader!./../excel/Blob');
require('script-loader!xlsx/dist/xlsx.core.min');
function generateArray(table) {
    let out = [];
    let rows = table.querySelectorAll('tr');
    let ranges = [];
    for (let R = 0; R < rows.length; ++R) {
        let outRow = [];
        let row = rows[R];
        let columns = row.querySelectorAll('td');
        for (let C = 0; C < columns.length; ++C) {
            let cell = columns[C];
            let colspan = cell.getAttribute('colspan');
            let rowspan = cell.getAttribute('rowspan');
            let cellValue = cell.innerText;
            if (cellValue !== "" && cellValue == +cellValue) cellValue = +cellValue;

            //Skip ranges
            ranges.forEach(function (range) {
                if (R >= range.s.r && R <= range.e.r && outRow.length >= range.s.c && outRow.length <= range.e.c) {
                    for (let i = 0; i <= range.e.c - range.s.c; ++i) outRow.push(null);
                }
            });

            //Handle Row Span
            if (rowspan || colspan) {
                rowspan = rowspan || 1;
                colspan = colspan || 1;
                ranges.push({s: {r: R, c: outRow.length}, e: {r: R + rowspan - 1, c: outRow.length + colspan - 1}});
            }
            ;

            //Handle Value
            outRow.push(cellValue !== "" ? cellValue : null);

            //Handle Colspan
            if (colspan) for (let k = 0; k < colspan - 1; ++k) outRow.push(null);
        }
        out.push(outRow);
    }
    return [out, ranges];
};

