const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");
const search = document.querySelector(".input-group input"),
  table_rows = document.querySelectorAll("tbody tr"),
  table_headings = document.querySelectorAll("thead th");

// show sidebar
menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});

// close sidebar
closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});

// change theme
themeToggler.addEventListener("click", () => {
  document.body.classList.toggle("dark-theme-variables");

  themeToggler.querySelector("span:nth-child(1)").classList.toggle("active");
  themeToggler.querySelector("span:nth-child(2)").classList.toggle("active");
});

// Events
const tabs = document.querySelectorAll("[data-tab-target]");
const tabContents = document.querySelectorAll("[data-tab-content]");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = document.querySelector(tab.dataset.tabTarget);
    tabContents.forEach((tabContent) => {
      tabContent.classList.remove("active-tab");
    });
    tabs.forEach((tab) => {
      tab.classList.remove("activ");
    });
    tab.classList.add("activ");
    target.classList.add("active-tab");
  });
});

// search
search.addEventListener("input", searchTable);

function searchTable() {
  table_rows.forEach((row, i) => {
    let table_data = row.textContent.toLowerCase(),
      search_data = search.value.toLowerCase();

    row.classList.toggle("hide", table_data.indexOf(search_data) < 0);
    row.style.setProperty("--delay", i / 25 + "s");
  });
  document.querySelectorAll("tbody tr:not(.hide)").forEach((visible_row, i) => {
    visible_row.style.backgroundColor =
      i % 2 == 0 ? "transparent" : "var(--color-white)";
  });
}

// table headeings

// table_headings.forEach((head, i) => {
//   let sort_asc = true;
//   head.onClick = () => {
//     table_headings.forEach(head => head.classList.remove('active'));
//     head.classList.add('active');

//     document.querySelectorAll('td').forEach(td => td.classList.remove('active'))
//     table_rows.forEach(row => {
//       row.querySelectorAll('td')[i].classList.add('active')
//     })
//     head.classList.toggle('asc', sort_asc);
//     sort_asc = head.classList.contains('asc') ? false : true;
//   }
// })

// converting html to pdf
const pdf_btn = document.querySelector("#toPDF");
// const customers_table = document.querySelector('#customers_table');
const customers_table = document.querySelector("#table_custom");

// function pdfGenerator(printableArea) {
//   var mywindow = window.open("", "PDF");

//   mywindow.document.write("<html><head>");
//   mywindow.document.write(
//     "<style>\n" +
//       "table {\n" +
//       "  border-collapse: collapse;\n" +
//       "  border-spacing: 0;\n" +
//       "  width: 100%;\n" +
//       "  border: 1px solid #ddd;\n" +
//       "}\n" +
//       "\n" +
//       "th, td {\n" +
//       "  text-align: left;\n" +
//       "  padding: 16px;\n" +
//       "}\n" +
//       "\n" +
//       "tr:nth-child(even) {\n" +
//       "  background-color: #f2f2f2;\n" +
//       "}\n"
//       +
//       ".html2canvas-container { width: 3000px !important; height: 3000px !important; }\n"
//       + "</style>"
//   );
//   var allRows = printableArea.getElementsByTagName("table")[0].rows;
//   for (var i = 0; i < allRows.length; i++) {
//     allRows[i].deleteCell(-1);
//   }
//   mywindow.document.write("</head><body >");
//   mywindow.document.write(
//     `<div class="table">${printableArea.innerHTML}</div>`
//   );
//   mywindow.document.write("</body></html>");
//   mywindow.document.close();
//   html2canvas(
//     mywindow.document.getElementsByTagName("body")[0],
//     {

//       onrendered: function (canvas) {
//         mywindow.close();
//         var imgData = canvas.toDataURL("image/png");
//         var newwindow = window.open(imgData);
//         var imgWidth = 210;
//         var pageHeight = 295;
//         var imgHeight = (canvas.height * imgWidth) / canvas.width;
//         var heightLeft = imgHeight;
//         var doc = new jsPDF("p", "mm");
//         var position = 0; // give some top padding to first page

//         doc.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
//         heightLeft -= pageHeight;

//         while (heightLeft >= 0) {
//           position += heightLeft - imgHeight; // top padding for other pages
//           console.log(imgData)
//           doc.addPage();
//           doc.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
//           heightLeft -= pageHeight;
//         }
//         doc.save("file.pdf");

//       },
//       allowTaint: true,
//       useCORS: true,
//       logging: false,

//     }

//     // allowTaint:true,
//     // useCORS: true,
//     // width:320,
//     // height:220
//   );

//   // mywindow.focus();
//   // mywindow.print();
//   // mywindow.close();
//   return true;
// }

// const toPDF = function (customers_table) {
//   const html_code = `
//     <link rel="stylesheet" href="./reports.css" >
//     <div class="table pagebreak">${customers_table.innerHTML}</div>
//   `;

//   const new_window = window.open();
//   new_window.document.write(html_code);

//   setTimeout(() => {
//     new_window.print();
//     new_window.close();
//   }, 200);
// }
var img_for_pdf = new Image()
img_for_pdf.src = '/static/homepage/pandgpic.png'
var img1_for_pdf  = new Image()
img1_for_pdf.src = '/static/homepage/consolepic.png'

function pdfGenerator(fileName) {
  console.log("Generating");
  var head;
  var doc = new jsPDF("l", "pt", "a4");
  var currentdate = new Date()
  
  // get the HTML table element
  // var table = document.getElementById(tableId);
  var visible_row = $('tr').filter(function() {
    return $(this).css('display') !== 'none';
  })
  
  //adding png image
  doc.addImage(img_for_pdf , 'png', 40, 40, 80, 80)

  //adding heading 
  doc.setTextColor(6,69,173);
  doc.setDrawColor(6,69,173);
  doc.setFontSize(16);
  doc.setFont("Calibri Light", "bold")
  doc.text(290, 90, "PRODUCT INSPECTION REPORT");
  doc.line(290, 92, 545, 92);

  //adding auto generated text
  doc.setDrawColor(0, 0, 0);
  doc.setTextColor(0,0,0);
  doc.setFontSize(11);
  doc.setFont("Calibri (Body)", "bold")
  // doc.text(265, 102, "Auto generated report by console");
  doc.text(300, 102, "Auto generated report by console");

  //adding console image
  doc.addImage(img1_for_pdf , 'png', 680, 50, 120, 50)

  //adding date                                               Date : 16-jun-23 
  doc.setFontSize(14);
  doc.setFont("Times", "bold")
  doc.text(50, 165, "Date: " + currentdate.getDate() + "-" + currentdate.toLocaleString('default', { month: 'short' }) + "-" + currentdate.getFullYear());

  //adding time
  doc.setFontSize(14);
  doc.setFont("Times", "bold")
  doc.text(650, 165, "Time: " + ((currentdate.getHours() < 10)?"0":"") + currentdate.getHours() +":"+ ((currentdate.getMinutes() < 10)?"0":"") + currentdate.getMinutes() +":"+ ((currentdate.getSeconds() < 10)?"0":"") + currentdate.getSeconds());

  // set the starting point for the table
  var x = 50;
  var y = 200;
  doc.setFont("Times", "normal")
  // define the row height and column width
  var rowHeight = 20;
  var colWidth = 150;
  var count = 0;
  // loop through each row in the table
  for (var i = 0; i < visible_row.length; i++) {
    if (i == 0) {
      head = visible_row[i].textContent.trim().split("\n");
      head.pop();
    }

    // loop through each column in the row
    for (var j = 0; j < visible_row[i].cells.length - 1; j++) {
      // get the cell content and add it to the PDF
      var cellText = visible_row[i].cells[j].textContent.trim();
      var cellWidth = j == 0 ? colWidth * 1 : colWidth;

      // split the cell text into multiple lines if it is too long
      var textLines = doc.splitTextToSize(cellText, cellWidth);

      // calculate the height required for the cell
      var cellHeight = rowHeight * textLines.length;

      // set the font size for the cell based on the number of lines
      var fontSize = textLines.length > 1 ? 10 : 12;
      if(i==0){
        doc.setFont("Times", "bold")
        doc.setFontSize(14);
      }
      else{
        doc.setFont("Times", "normal")
        doc.setFontSize(fontSize);
      }

      // add the cell content to the PDF
      doc.text(x, y + rowHeight, textLines);

      // increment the x position for the next cell
      x += cellWidth;
    }

    // reset the x position and increment the y position for the next row
    x = 50;
    y += rowHeight;

    // check if the page needs to be added for long tables
    if (y + rowHeight >= doc.internal.pageSize.height - 50) {
      doc.addPage();
      y = 50;
      for (var k = 0; k < head.length; k++) {
        var cellText = head[k].trim();
        var cellWidth = k == 0 ? colWidth * 1 : colWidth;
        // split the cell text into multiple lines if it is too long
        var textLines = doc.splitTextToSize(cellText, cellWidth);

        // calculate the height required for the cell
        var cellHeight = rowHeight * textLines.length;

        // set the font size for the cell based on the number of lines
        var fontSize = textLines.length > 1 ? 10 : 12;
        // doc.setFontSize(fontSize);
        doc.setFont("Times", "bold")
        doc.setFontSize(14);

        // add the cell content to the PDF
        doc.text(x, y + rowHeight, textLines);

        // increment the x position for the next cell
        x += cellWidth;
      }
      x = 50;
      y += rowHeight;
    }
  }

  // save the PDF file
  doc.save(fileName + ".pdf");
}

pdf_btn.onclick = () => {
  // toPDF(customers_table);
  pdfGenerator("file");
};

// converting html to excel

const excel_btn = document.querySelector("#toEXCEL");

const toExcel = function () {
  const t_rows = $('tr').filter(function() {
    return $(this).css('display') !== 'none';
  })
  return [...t_rows]
    .map((row) => {
      const cells = row.querySelectorAll("th, td");
      var nodes = [].slice.call(cells, 0);
      nodes.pop()
      return [...nodes].map((cell) => cell.textContent.trim()).join("\t");
    })
    .join("\n");
};

excel_btn.onclick = () => {
  const excel = toExcel();
  downloadFile(excel, "excel", "inspection report.xls");
};

// converting html to csv

const csv_btn = document.querySelector("#toCSV");

const toCSV = function () {
  
  const t_rows = $('tr').filter(function() {
    return $(this).css('display') !== 'none';
  })
  console.log(t_rows)
  return [...t_rows]
    .map((row) => {
      const cells = row.querySelectorAll("th, td");
      var nodes = [].slice.call(cells, 0);
      nodes.pop()
      return [...nodes].map((cell) => cell.textContent.trim()).join(",");
    })
    .join("\n");
};

csv_btn.onclick = () => {
  const csv = toCSV();
  downloadFile(csv, "csv", "inspection report.csv");
};

// downloading main

const downloadFile = function (data, fileType, fileName) {
  const a = document.createElement("a");
  a.download = fileName;
  const mime_types = {
    json: "application/json",
    excel: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    csv: "text/csv",
  };
  a.href = `
    data:${mime_types[fileType]};charset=utf-8,${encodeURIComponent(data)}
  `;
  document.body.appendChild(a);
  a.click();
  a.remove();
};

// html table print

const print_btn = document.querySelector("#toPRINT");

function printPageArea(printableArea) {
  var mywindow = window.open("", "PRINT");

  mywindow.document.write("<html><head>");
  mywindow.document.write(
    "<style>\n" +
      "table {\n" +
      "  border-collapse: collapse;\n" +
      "  border-spacing: 0;\n" +
      "  width: 100%;\n" +
      "  border: 1px solid #ddd;\n" +
      "}\n" +
      "\n" +
      "th, td {\n" +
      "  text-align: left;\n" +
      "  padding: 16px;\n" +
      "}\n" +
      "\n" +
      "tr:nth-child(even) {\n" +
      "  background-color: #f2f2f2;\n" +
      "}</style>"
  );
  
  var allRows = $('tr').filter(function() {
    return $(this).css('display') !== 'none';
  })
  var html_table = `<div class="table"> <table id="tabular_form"><thead>`;
  html_table+=`<tr>`
  for(var i = 0; i < 5; i++){
    html_table+=`${allRows[0].cells[i].outerHTML}`;
  }
  html_table+=`</tr>`
  html_table+=`</thead>`
  html_table+=`<tbody>`
  
  for (var i = 1; i < allRows.length; i++) {
    html_table+=`<tr>`

    html_table+=`${allRows[i].cells[0].outerHTML}`
    html_table+=`${allRows[i].cells[1].outerHTML}`
    html_table+=`${allRows[i].cells[2].outerHTML}`
    html_table+=`${allRows[i].cells[3].outerHTML}`
    html_table+=`${allRows[i].cells[4].outerHTML}`
    
    html_table+=`</tr>`
    
    
  }
  
  html_table+=`</tbody>`
  html_table+=`</table></div>`
  // for (var i = 0; i < allRows.length; i++) {
  //   console.log(allRows[i].cells[2]);
  //   if(i>3){break;}
  // }
  
  // console.log(printableArea.innerHTML);
  // return true;
  mywindow.document.write("</head><body >");
  mywindow.document.write(
    `<div class="table">${html_table}</div>`
  );
  // mywindow.document.write(
  //   `<div class="table">${printableArea.innerHTML}</div>`
  // );
  mywindow.document.write("</body></html>");

  mywindow.document.close();

  mywindow.focus();
  mywindow.print();
  mywindow.close();
  return true;
}

// const toPRINT = function (customers_table) {
//   const html_code = `
//     <link rel="stylesheet" href="./reports.css">
//     <div class="table">${customers_table.outerHTML}</div>
//   `;

//   const new_window = window.open();
//   new_window.document.write(html_code);

//   setTimeout(() => {
//     new_window.print();
//     new_window.close();
//   }, 200);
// }

print_btn.onclick = () => {
  printPageArea(customers_table);
};


const mail_btn = document.querySelector("#toMail");

function mail_doc(){

  var head;
  var doc = new jsPDF("l", "pt", "a4");

  var visible_row = $('tr').filter(function() {
    return $(this).css('display') !== 'none';
  })

    //adding png image
  doc.addImage(img_for_pdf , 'png', 40, 40, 80, 80)

  //adding heading 
  doc.setTextColor(6,69,173);
  doc.setDrawColor(6,69,173);
  doc.setFontSize(16);
  doc.setFont("Calibri Light", "bold")
  doc.text(290, 90, "PRODUCT INSPECTION REPORT");
  doc.line(290, 92, 545, 92);

  //adding auto generated text
  doc.setDrawColor(0, 0, 0);
  doc.setTextColor(0,0,0);
  doc.setFontSize(11);
  doc.setFont("Calibri (Body)", "bold")
  // doc.text(265, 102, "Auto generated report by console");
  doc.text(300, 102, "Auto generated report by console");

  //adding console image
  doc.addImage(img1_for_pdf , 'png', 680, 50, 120, 50)

  //adding date                                               Date : 16-jun-23 
  doc.setFontSize(14);
  doc.setFont("Times", "bold")
  doc.text(50, 165, "Date: " + currentdate.getDate() + "-" + currentdate.toLocaleString('default', { month: 'short' }) + "-" + currentdate.getFullYear());

  //adding time
  doc.setFontSize(14);
  doc.setFont("Times", "bold")
  doc.text(650, 165, "Time: " + ((currentdate.getHours() < 10)?"0":"") + currentdate.getHours() +":"+ ((currentdate.getMinutes() < 10)?"0":"") + currentdate.getMinutes() +":"+ ((currentdate.getSeconds() < 10)?"0":"") + currentdate.getSeconds());

  // set the starting point for the table
  var x = 50;
  var y = 200;
  doc.setFont("Times", "normal")
  // define the row height and column width
  var rowHeight = 20;
  var colWidth = 150;
  var count = 0;
  
  // loop through each row in the table
  for (var i = 0; i < visible_row.length; i++) {
    if (i == 0) {
      head = visible_row[i].textContent.trim().split("\n");
      head.pop();
    }

    // loop through each column in the row
    for (var j = 0; j < visible_row[i].cells.length - 1; j++) {
      // get the cell content and add it to the PDF
      var cellText = visible_row[i].cells[j].textContent.trim();
      var cellWidth = j == 0 ? colWidth * 1 : colWidth;

      // split the cell text into multiple lines if it is too long
      var textLines = doc.splitTextToSize(cellText, cellWidth);

      // calculate the height required for the cell
      var cellHeight = rowHeight * textLines.length;

      // set the font size for the cell based on the number of lines
      var fontSize = textLines.length > 1 ? 10 : 12;
      if(i==0){
        doc.setFont("Times", "bold")
        doc.setFontSize(14);
      }
      else{
        doc.setFont("Times", "normal")
        doc.setFontSize(fontSize);
      }

      // add the cell content to the PDF
      doc.text(x, y + rowHeight, textLines);

      // increment the x position for the next cell
      x += cellWidth;
    }

    // reset the x position and increment the y position for the next row
    x = 50;
    y += rowHeight;

    // check if the page needs to be added for long tables
    if (y + rowHeight >= doc.internal.pageSize.height - 50) {
      doc.addPage();
      y = 50;
      for (var k = 0; k < head.length; k++) {
        var cellText = head[k].trim();
        var cellWidth = k == 0 ? colWidth * 1 : colWidth;
        // split the cell text into multiple lines if it is too long
        var textLines = doc.splitTextToSize(cellText, cellWidth);

        // calculate the height required for the cell
        var cellHeight = rowHeight * textLines.length;

        // set the font size for the cell based on the number of lines
        var fontSize = textLines.length > 1 ? 10 : 12;
        // doc.setFontSize(fontSize);
        doc.setFont("Times", "bold")
        doc.setFontSize(14);

        // add the cell content to the PDF
        doc.text(x, y + rowHeight, textLines);

        // increment the x position for the next cell
        x += cellWidth;
      }
      x = 50;
      y += rowHeight;
    }
  }
  var pdfBase64 = doc.output('datauristring');
  
  Email.send({
    Host : "smtp.elasticemail.com",
    Username : "syedmuhammad3333@gmail.com",
    Password : "3BA74F23DECFD619C35523461478507823F5",
    To : 'basrahafeez@gmail.com',
    From : "syedmuhammad3333@gmail.com",
    Subject : "This is the file",
    Body : "message goes here!",
    Attachments : [
      {
       name : "list.pdf",
       data : pdfBase64 
 
      }],
}).then(
  message => alert("Email sent!")
  // Do any function after email sent
  
);


}

mail_btn.onclick = () => {
  mail_doc();
};