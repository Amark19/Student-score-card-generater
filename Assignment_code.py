from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.legends import Legend
from reportlab.platypus import Paragraph, Image, Table
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import pagesizes
from reportlab.lib.validators import Auto
import pandas as pd
try:

    df=pd.read_csv("Dummy Data for final assignment.csv")
    width=  1000
    height = 1100
    Alls_marks=[]#collecting marks of all the students to put it into bar graph
    Alls_register=[]#collecting registration no of all the students to put it into bar graph
    total_rows=df.shape[0]
    per_student_offset=25
    for Alls in range(0,total_rows//per_student_offset):
        Alls_marks.append(df['Your score'][Alls*per_student_offset:Alls*per_student_offset+25].sum())
        Alls_register.append(df['Registration Number'][Alls*per_student_offset])

    def count_percentile(marks):
        count=0
        for mark in Alls_marks:
            if mark<=marks:
                count+=1
        
        return (count / 5)*100
    def drawPieChart(pc,d,x,y,width,height,data_str,labels,can,data):
        pc.x = x
        pc.y = y
        pc.width = width
        pc.height = height
        pc.data = data
        pc.labels = data_str
        pc.slices.strokeWidth=0.5
        d.add(pc)
        d.drawOn(can,0,0)
        
        can.setFont("Helvetica-Oblique",10)
        can.setFillColor(colors.green)
        y-=30
        can.drawString(x+10,y,"Total Qs : 25")
        y-=30
        
        for i in range(len(labels)):
            can.drawString(x+10,y,f"{labels[i]} : {data[i]}")
            y-=30
        
    def create_pdf(pdf_file,row_range,col_range_for_table,row_init,st1_details,bg_img,cont,cont_1):
        
        can = canvas.Canvas(pdf_file,pagesize=pagesizes.A4)
        ##************************************PAGE1*******************************************
        can.setPageSize((800,1000))
        score = df['Your score'][row_init:row_init+25].sum()
        logo_img="logo.png"
        pathSt_img=f"static/Pics for assignment/{st1_details['Sname'][row_init]}.png"
        can.drawImage(bg_img,0,0,width=width,height=height , preserveAspectRatio=True, mask='auto')
        #title
        can.setFillColor(colors.black)
        can.setFont("Helvetica-Bold",15)
        can.drawString(200,900, "INTERNATIONAL MATHS OLYMPIAD CHALLENGE")
        can.drawImage(logo_img,280,790,width=200,height=100, preserveAspectRatio=True, mask='auto')
        can.drawString(230, 750, f"Round 2 performance of {st1_details['Sname'][row_init]}")
        can.drawImage(pathSt_img,570,690, width=170,height=270, preserveAspectRatio=True, mask='auto')
        student_detail = (
        ("Grade", f"{st1_details['Grade'][row_init]}", "", "Registration No. ", f"{int(st1_details['RegisNo'][row_init])}"),
        ("School Name", f"{st1_details['schoolN'][row_init]}", "", "Gender", f"{st1_details['Gender'][row_init]}"),
        ("City Of Residence", f"{st1_details['city'][row_init]}", "", "Date of Birth",
         f"{st1_details['DOB'][row_init]}"),
        ("Country Of Residence", f"{st1_details['country'][row_init]}", "", "Date Of Test",
         f"5-6 august 2021")
        )
        tbl_style = (
            ('FONT', (0, 0), (0, -1), "Helvetica-Bold"),
            ('FONT', (3, 0), (3, -1), "Helvetica-Bold"),
            ('INNERGRID', (0, 0), (1, -1), 1, (0, 0, 0)),
            ('INNERGRID', (-2, 0), (-1, -1), 1, (0, 0, 0)),
            ('BOX', (0, 0), (1, -1), 1, (0, 0, 0)),
            ('BOX', (-2, 0), (-1, -1), 1, (0, 0, 0)),
        )
        table = Table(student_detail, style=tbl_style, colWidths=(None, 5 * cm, 1 * cm, None, 5 * cm))
        w, h = table.wrapOn(can, 0, 0)
        table.drawOn(can,130,630)
        can.setFont("Helvetica-Oblique",15)
        can.drawString(370, 580, "Section - 1")
        can.setFont("Helvetica",12)
        can.drawString(210, 550, f"This section describes {st1_details['Sname'][row_init]} performance v/s the Test in Grade {st1_details['Grade'][row_init]}")
        
        report_table_data = [
        ("Question No.", f"What you marked?", 'Correct Answer',
         'Outcome', 'Score if correct', "Your Score"),
        ]

        rec=cont[cont['Registration Number'] == int(st1_details['RegisNo'][row_init]) ]
        # print(int(st1_details['RegisNo'][row_init]))
        for _, row in rec.iterrows():
            report_table_data.append((
                row['Question No.'],  row['What you marked'], row['Correct Answer'],
                row['Outcome (Correct/Incorrect/Not Attempted)'],
                row['Score if correct'], row['Your score']
            ))
        style = (
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), (0, 0, 0)),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('BOX', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0))
        )
        table1 = Table(report_table_data, style=style)
        w, h = table1.wrapOn(can, 0, 0)
        table1.drawOn(can,150,50)
        
        can.setFont("Helvetica-Bold",10)
        can.drawString(500, 30, f"Total Score : {score}")
        can.showPage()
        ##***********************************************PAGE2*********************************************

        #SCORECARD
        can.setPageSize((800,1000))
        can.drawImage(bg_img,0,0,width=width,height=height, preserveAspectRatio=True, mask='auto')
        can.setFont("Helvetica-Oblique",15)
        can.drawString(370, 950, "Section - 2")
        can.setFont("Helvetica",12)
        can.drawString(200, 920, f"This section describes {st1_details['Sname'][row_init]} performance v/s rest of the world in Grade {st1_details['Grade'][row_init]}")
        
        report_table_data_1= [
        ("Question No.", f"What u\nmarked?", 'Correct\nAnswer',
         'Outcome', 'Score if\ncorrect', "Your\nScore","% of students\nacross the world\nwho attempted\nthis question",
         "% of students (from\nthose who attempted\nthis ) who got it\ncorrect",
         "% of students\n(from those who\nattempted this)\nwho got it\nincorrect",
         "World Average\nin this question"
         
         
         
         ),
        ]

        rec_1=cont_1[cont_1['Registration Number'] == int(st1_details['RegisNo'][row_init]) ]
        # print(int(st1_details['RegisNo'][row_init]))
        for _, row in rec_1.iterrows():
            report_table_data_1.append((
                row['Question No.'],  row['What you marked'], row['Correct Answer'],
                row['Outcome (Correct/Incorrect/Not Attempted)'],
                row['Score if correct'], row['Your score'],
                row['% of students\nacross the world\nwho attempted\nthis question'],
                row['% of students (from\nthose who attempted\nthis ) who got it\ncorrect'],
                row['% of students\n(from those who\nattempted this)\nwho got it\nincorrect'],
                row['World Average\nin this question\n']
                # row['World Average\nin this question'],
            ))
        style = (
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), (0, 0, 0)),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('BOX', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0))
        )
        table2 = Table(report_table_data_1, style=style)
        w, h = table2.wrapOn(can, 0, 0)
        table2.drawOn(can,40,380)
        print(score,count_percentile(score))
        
        
        # can.setFont("Helvetica-Oblique",30)
        # can.setFillColor(colors.red)

        # can.drawString(100,800,"Student Scorecard and analysis")
        # can.setFillColor(colors.orange)
        # can.setFont("Helvetica-Oblique",10)

        # Total_marks=100
        # Total_score_student=df['Your score'][row_init:row_init+25].sum()
        # corrected_answer=0
        # uncorrected_ans=0
        # Not_attempted=0
        # for outc in df['Outcome (Correct/Incorrect/Not Attempted)'][row_init:row_init+25]:
        #     if outc=="Correct":
        #         corrected_answer+=1
        #     elif outc=="Incorrect":
        #         uncorrected_ans+=1
        #     else:
        #         Not_attempted+=1
        

        # can.setFont("Helvetica-Oblique",15)
        # can.setFillColor(colors.orange)
        # can.drawString(180,750,f"Student Score :  {Total_score_student} / 100")
        # can.drawString(100,715,f"{df['Qualification'][row_init]}")
        # can.setFillColor(colors.black)
        # can.line(30,705,550,705)
        # #Analysis using piechart
    
        # can.setFont("Helvetica-Oblique",15)
        # can.setFillColor(colors.black)
        # can.drawString(80,680,"Question Analysis")
        # d = Drawing(200, 100)
    
        # pc = Pie()
    
        # pc.sideLabels=True
        # x1=80
        # y1=550
        # width1=100
        # height1=100
        # data1=[Not_attempted,25-Not_attempted]
        # data_str1=[str(Not_attempted),str(25-Not_attempted)]
        # labels1=['Unattempted Qs',"Attempted Qs"]
        # drawPieChart(pc,d,x1,y1,width1,height1,data_str1,labels1,can,data1)
        
        # ##Piechart 2
        # can.setFillColor(colors.black)
        # can.setFont("Helvetica-Oblique",15)
        # can.drawString(400,680,"Solution Analysis")
        # x1=400
        # y1=545
        # width1=100
        # height1=100
        # data1=[uncorrected_ans,corrected_answer,Not_attempted]
        # data_str1=[str(uncorrected_ans),str(corrected_answer),str(Not_attempted)]
        # labels1=["Uncorrect answers","Correct answers","Not attempted"]
        # drawPieChart(pc,d,x1,y1,width1,height1,data_str1,labels1,can,data1)
        
        # ##Comparision bar graph

        # can.setFillColor(colors.black)
        # can.setFont("Helvetica-Oblique",25)
        # can.drawString(230,350,"Comparision")
        # data_all = []
        # names_list=[]
        # for j in range(len(Alls_register)):
        #     if Alls_register[j]!=st1_details['RegisNo'][row_init]:
        #         data_all.append(Alls_marks[j])
        #         names_list.append(df['Full Name '][j*25])
            

        # data_all.insert(0,Total_score_student)
        # names_list.insert(0,"You")
        # # print(Alls_names)
        # d=Drawing(400,200)
        # bc = VerticalBarChart()
        
        # bc.x = 150
        # bc.y = 100
        # bc.height = 300
        # bc.width = 300
        # bc.data = [(data_all)]
        # bc.strokeColor = colors.black
        # bc.valueAxis.valueMin = 0
        # bc.valueAxis.valueMax = 100
        # bc.valueAxis.valueStep = 30
        # bc.categoryAxis.labels.boxAnchor = 'ne'
        # bc.categoryAxis.labels.dx = 8
        # bc.categoryAxis.labels.dy = -2
        # bc.categoryAxis.labels.angle = 30
        # bc.categoryAxis.categoryNames = names_list
        # d.add(bc)
        # # d.wrapOn(can,400,200    can=
        # d.drawOn(can,10,10)
        
        # print(ca)
        can.showPage()

    
        ##***********************************************PAGE3********************************************* 
        ##if student want to see records and details of each question then records of table can be displayed by folowing code
        ##all details of exam with marked qs and its response
        can.setFillColor(colors.red)
        can.setFont("Helvetica-Oblique",30)
        can.drawString(150,800, "Student Test records")
        can.setFont("Helvetica-Oblique",12)
        can.setFillColor(colors.orange)
        
        can.drawString(50,750, "Below there are the responses of each question which was in the test given by the student. ")
        
        
        #column list
        can.setFillColor(colors.red)

        column_name=['Qs no','Marked ans' ,'correct ans' , 'Outcome' , 'score if correct' ,'Your score']##shortend names of columns due to unavailable space
        ##declaring variables 
        
        col_x_value=75
        col1_x_value=70
        table_y1_top_value=720
        table_x2_right_value=590
        can.line(col1_x_value, table_y1_top_value, table_x2_right_value, table_y1_top_value)
        for colm in column_name:
            # print(colm)
            can.drawString(col_x_value,700, colm)
            col_x_value+=90
        table_x_value=80
        can.line(col1_x_value, 685, table_x2_right_value, 685)
        can.setFillColor(colors.green)
        for nexCol_value in range(len(col_range_for_table)):
            table_y_value=670
            row=[]
            for nexRow_value in range(row_init,row_init+25):
                value=str(row_range[col_range_for_table[nexCol_value]][nexRow_value])
                can.drawString(table_x_value, table_y_value, value)#value placed in given position
                table_y_value-=20
                can.line(col1_x_value, table_y_value+15, table_x2_right_value, table_y_value+15)##these are to create table outline
            can.line(table_x_value-10, table_y1_top_value, table_x_value-10, 180)
            
            table_x_value+=90
        can.line(table_x2_right_value, table_y1_top_value, table_x2_right_value, 180)
        
        can.showPage()
    
        
    
        can.save()


    ##global info
    cont = df[['Question No.', 'What you marked', 'Correct Answer',
                 'Outcome (Correct/Incorrect/Not Attempted)', 'Score if correct',
                 'Your score'] + ['Country of Residence', 'Registration Number']]
    cont_1 = df[['Question No.', 'What you marked', 'Correct Answer',
                 'Outcome (Correct/Incorrect/Not Attempted)', 'Score if correct',
                 'Your score','% of students\nacross the world\nwho attempted\nthis question',
       '% of students (from\nthose who attempted\nthis ) who got it\ncorrect',
       '% of students\n(from those who\nattempted this)\nwho got it\nincorrect',
       'World Average\nin this question\n',
                    ] + ['Country of Residence', 'Registration Number']]

    students_col_range_table=df.columns[13:19]
    row_init_value=0       
    no_of_student = 5  
    bg_img="back.png"
    st_details={"Sname":df[df.columns[4]],"Grade":df[df.columns[6]],"RegisNo":df[df.columns[5]],
                "schoolN":df[df.columns[7]],"DOB":df[df.columns[9]],"Gender":df[df.columns[8]],"country":df[df.columns[12]] , 
                "city":df[df.columns[10]]  }#collecting details of students in dict
    
    #creating pdf for each student
    for student in range(no_of_student):
        student_row_range = df.iloc[row_init_value:row_init_value + 25]
        create_pdf(f"student {student + 1}.pdf",student_row_range,students_col_range_table,row_init_value,st_details,bg_img,cont,cont_1)
        row_init_value +=25
    print("Scorecard PDF's have been created succesfully!")
except Exception as e:
    print(e)