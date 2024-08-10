from bs4 import BeautifulSoup
import pandas as pd


with open('cjcx_list.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

df = pd.DataFrame(columns=['课程名', '成绩', '学分','课程类型'])
cl = [ '必修','限选']
trs = soup.find_all('tr')

total_score = 0
total_credit = 0

for tr in trs:
    tds = tr.find_all('td')
    
    if len(tds) > 13:
        course_name = tds[3].get_text(strip=True)
        
        score = tds[4].find('a').get_text(strip=True) if tds[4].find('a') else None
        score = pd.to_numeric(score, errors='coerce')
        credit = tds[6].get_text(strip=True)
        credit = pd.to_numeric(credit, errors='coerce')
        course_category = tds[12].get_text(strip=True)
        print(f'课程名: {course_name}, 成绩: {score}, 学分: {credit}, 课程类型：{course_category}')
        
        if course_category in cl:
            total_score = total_score + credit * score
            total_credit = total_credit + credit
            temp_df = pd.DataFrame({
                '课程名': [course_name],
                '成绩': [score],
                '学分': [credit],
                '课程类型': [course_category]
            })
            
            df = pd.concat([df, temp_df], ignore_index=True)
        
df.to_excel('output.xlsx', index=False)
print('\n\r'+'*'*50)
print(f'\n\r总学分：{total_credit},学分绩：{total_score/total_credit}')
