import pandas as pd
import os

# Читаем CSV
df = pd.read_csv('evaluation/tourism_travel_questions_with_ground_truth_ver_short.csv')


# Обрабатываем каждый вопрос
for i, row in df.iterrows():
    question = row['question']
    print(f"\n[{i+1}/{len(df)}] Запуск: {question[:50]}...")
    
    
    # Формируем команду
    cmd = f'python ./team-repo/AI\ guide/main.py --q "{question}" --save'
    
    # Выполняем
    os.system(cmd)
    
print(f"\n✅ Готово! Обработано {len(df)} вопросов.")