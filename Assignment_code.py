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
    
    def Drawtable(detail,x,y,can,colwid):
        tbl_style = (
            ('FONT', (0, 0), (0, -1), "Helvetica-Bold"),
            ('FONT', (3, 0), (3, -1), "Helvetica-Bold"),
            ('INNERGRID', (0, 0), (1, -1), 1, (0, 0, 0)),
            ('INNERGRID', (-2, 0), (-1, -1), 1, (0, 0, 0)),
            ('BOX', (0, 0), (1, -1), 1, (0, 0, 0)),
            ('BOX', (-2, 0), (-1, -1), 1, (0, 0, 0)),
        )
        table = Table(detail, style=tbl_style, colWidths=colwid)
        w, h = table.wrapOn(can, 0, 0)
        table.drawOn(can,x,y)
    
    def Drawbargraph(data,labels,x,y,width,height,can):
        d=Drawing(400,200)
        bc = VerticalBarChart()
        
        bc.x = x
        bc.y = y
        bc.height = height
        bc.width = width
        bc.data = [(data)]
        bc.strokeColor = colors.black
        bc.bars[0].fillColor = colors.blue
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 30
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = labels
        d.add(bc)
        # d.wrapOn(can,400,200    can=
        d.drawOn(can,10,10)

    def create_pdf(pdf_file,row_range,col_range_for_table,row_init,st1_details,bg_img,cont,cont_1):
        
        can = canvas.Canvas(pdf_file,pagesize=pagesizes.A4)
        ##************************************PAGE1*******************************************
        can.setPageSize((800,1000))
        score = df['Your score'][row_init:row_init+25].sum()
        logo_img="logo.png"
        pathSt_img=f"static/Pics for assignment/{st1_details['Sname'][row_init]}.png"
        can.drawImage(bg_img,0,0,width=width,height=height , preserveAspectRatio=True, mask='auto')
        can.setFont("Helvetica",10)
        can.drawString(10,970, f"Round 2 - enhanced Score Report : {st1_details['Sname'][row_init]}")
        can.drawString(10,950, f"Registration Number : {int(st1_details['RegisNo'][row_init])}")

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
        
        Drawtable(student_detail,130,630,can,(None, 5 * cm, 1 * cm, None, 5 * cm))

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

        can.setFont("Helvetica",10)
        can.drawString(20, 360, f"{st1_details['Sname'][row_init]} overall percentile is {count_percentile(score)}% . This indicates that {st1_details['Sname'][row_init]} has scored more than {count_percentile(score)}%  of students in the World and lesser than {100 - count_percentile(score)}% of student in the world")
        can.setFont("Helvetica-Bold",15)
        can.drawString(50,320,"Overview")


        #table and its respective bar graph
        
        Avg_score = df['Average score of all students across the World'][row_init]
        Median = df['Median score of all students across the World'][row_init]
        Mode = df['Mode score of all students across World'][row_init]
        Data_bar_1 = [score , Avg_score , Median , Mode]
        Labels_1 = ['You' , 'Avg' , 'Median' , 'Mode']
        detail_1 = (
        ("Average score of all\nstudents across the World ", f"{Avg_score}"),
        ("Median score of all\nstudents across the World ", f"{Median}"),
        ("Mode score of all students across World ", f"{Mode}"),
        )
        
        Drawtable(detail_1,30,230,can,(None, 1.2 * cm))
        can.setFont("Helvetica",12)
        can.drawString(80,200,"Comparision Of Scores")
        Drawbargraph(Data_bar_1 , Labels_1 ,55,20,150,150,can)


        stu_attempt = df['First names attempts (Attempts x 100 / Total Questions)'][row_init]
        Avg_attempt = df['Average attempts of all students across the Worl'][row_init]
        Data_bar_2 = [stu_attempt , Avg_attempt]
        Labels_2 = ['You' , 'World']
        detail_2 = (
        (f"{st1_details['Sname'][row_init]}'s attempts\n(Attempts x 100 / Total Questions)  ", f"{stu_attempt}"),
        ("Average attempts of all\nstudents across the World ", f"{Avg_attempt}"),
        )
        
        Drawtable(detail_2,280,240,can,(None, 3 * cm))
        can.drawString(300,200,"Comparision Of Attempt(%)")
        Drawbargraph(Data_bar_2 , Labels_2 ,330,20,100,150,can)

        Stu_accu = df['First names Accuracy ( Corrects x 100 /Attempts )'][row_init]
        Avg_acc = df['Average accuracy of all students across the World'][row_init]
        Data_bar_3 = [float(str(Stu_accu)[:len(str(Stu_accu)) - 2]) , float(str(Avg_acc)[:len(str(Avg_acc)) - 2])]
        Labels_3 = ['You' , 'World']
        detail_3 = (
        (f"{st1_details['Sname'][row_init]}'s Accuracy\n( Corrects x 100 /Attempts ) ", f"{Stu_accu}"),
        ("Average accuracy of all\nstudents across the World ", f"{Avg_acc}"),
        )
        
        Drawtable(detail_3,550,240,can,(None, 3 * cm))
        can.drawString(540,200,"Comparision Of Accuracy(%)")
        Drawbargraph(Data_bar_3 , Labels_3 ,600,20,100,150,can)
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