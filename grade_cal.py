#Build a Student Grade Calculator that takes marks and returns grade with comments, and stores results in a list
result = []
def student_grade(marks) :
    if marks >= 90:
        return "o+", "outstanding"
    elif marks >= 80:
        return "A+", "excellent work"   
    elif marks >= 70:
        return "B+" "good"
    elif marks >= 60:
        return "c+", "keep improving"
    elif marks >= 50:
        return "D", "pass"
    else :
        return "F", "fail"
    
while True:
    marks = int(input("enter your marks between o to 100  :"))
    grade, comment = student_grade(marks)
    result = {
    "marks" : marks,
    "grade" : grade,
    "comment": comment
}
   
    print("result added:")
    print(result)
