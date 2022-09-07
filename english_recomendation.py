import pandas as pd #импорт данных
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer #мешок слов
from sklearn.feature_extraction.text import TfidfVectorizer # определить частоту слова
from sklearn.metrics import pairwise_distances #косинусное сходство


def SearchRecommendarion(txt1, txt2, txt3):
    error = ''
    df0 = pd.read_csv('Kniga-5.1.0.csv') 
    df1 = pd.read_csv('Kniga-5.1.1.csv') 
    df2 = pd.read_csv('Kniga-5.1.2.csv') 
    df3 = pd.read_csv('Kniga-5.1.3.csv') 
    df4 = pd.read_csv('Kniga-5.1.4.csv') 
    df = pd.concat([df0,df1,df2,df3,df4], ignore_index=True)
    # df = pd.read_csv("Textonator/Kniga-51.csv") #загружаем файл "C:\Users\Никита\Downloads\Textonator\Kniga-51.csv"

    title_1 = txt1
    title_2 = txt2
    title_3 = txt3
   
    liked_book_1 = df[df['title'] == title_1]
    liked_book_2 = df[df['title'] == title_2]
    liked_book_3 = df[df['title'] == title_3]



    if liked_book_1.empty:
        liked_book_1 = df[df['ru_title'] == title_1]
        ID_book_1 = df.loc[df['ru_title']==title_1].index[0]
    else: ID_book_1 = df.loc[df['title']==title_1].index[0]

    if liked_book_2.empty:
        liked_book_2 = df[df['ru_title'] == title_2]
        ID_book_2 = df.loc[df['ru_title']==title_2].index[0]
    else: ID_book_2 = df.loc[df['title']==title_2].index[0]

    if liked_book_3.empty:
        liked_book_3 = df[df['ru_title'] == title_3]
        ID_book_3 = df.loc[df['ru_title']==title_3].index[0]
    else: ID_book_3 = df.loc[df['title']==title_3].index[0]

    text_bow_book_1 = ''.join(liked_book_1['Lemmatized'])
    text_bow_book_2 = ''.join(liked_book_2['Lemmatized'])
    text_bow_book_3 = ''.join(liked_book_3['Lemmatized'])
    all_bow_books = []
    all_bow_books.append(text_bow_book_1)
    all_bow_books.append(text_bow_book_2)
    all_bow_books.append(text_bow_book_3)
    tfidf = TfidfVectorizer() #подбираем по частоте
    x_tfidf = tfidf.fit_transform(all_bow_books).toarray()
    df_tfidf = pd.DataFrame(x_tfidf, columns = tfidf.get_feature_names_out())

    persent_tfidf = 0

    book_1_tfidf = tfidf.transform([text_bow_book_1])
    cos_tfidf_book_1 = np.round(1 - pairwise_distances(df_tfidf, book_1_tfidf, metric= 'cosine'), 3)
    book_2_tfidf = tfidf.transform([text_bow_book_2])
    cos_tfidf_book_2 = np.round(1 - pairwise_distances(df_tfidf, book_2_tfidf, metric= 'cosine'), 3)
    ready_tfidf = [cos_tfidf_book_1[1][0], cos_tfidf_book_1[2][0], cos_tfidf_book_2[2][0]]
    if ready_tfidf[0] and ready_tfidf[1] and ready_tfidf[2] >= 0.5:
        koeff = max(ready_tfidf) - min(ready_tfidf) #Разница максимального с минимальным
        if koeff <= 0.4: persent_tfidf = 60
        if koeff <= 0.3: persent_tfidf = 70
        if koeff <= 0.2: persent_tfidf = 80
        if koeff <= 0.1: persent_tfidf = 90
    else:
        persent_tfidf = (ready_tfidf[0] + ready_tfidf[1] + ready_tfidf[2])/3*0.5*100
    cv = CountVectorizer()

    X = cv.fit_transform(all_bow_books).toarray()#перевели в массив
    features = cv.get_feature_names_out()
    df_bow = pd.DataFrame(X, columns= features) #делаем мешок слов

    persent_bow = 0

    book_1_bow = cv.transform([text_bow_book_1]).toarray()
    cos_bow_book_1 = np.round(1 - pairwise_distances(df_bow, book_1_bow, metric= 'cosine'), 3)
    book_2_bow = cv.transform([text_bow_book_2]).toarray()
    cos_bow_book_2 = np.round(1 - pairwise_distances(df_bow, book_2_bow, metric= 'cosine'), 3)
    ready_bow = [cos_bow_book_1[1][0], cos_bow_book_1[2][0], cos_bow_book_2[2][0]]
    min_bow = min(ready_bow)
    if min_bow <= 0.9: persent_bow = 90
    if min_bow <= 0.8: persent_bow = 80
    if min_bow <= 0.7: persent_bow = 70
    if min_bow <= 0.6: persent_bow = 60
    if min_bow <= 0.5: persent_bow = 50
    if min_bow <= 0.4: persent_bow = 40
    if min_bow <= 0.3: persent_bow = 30
    if min_bow <= 0.2: persent_bow = 20
    if min_bow <= 0.1: persent_bow = 10


    df_tag = pd.read_csv('Tag_results_rus.csv')
    persent_tag = 0
    tag_koef = 1.275
    tag_book_1 = list(df_tag.iloc[ID_book_1][:])
    tag_book_2 = list(df_tag.iloc[ID_book_2][:])
    tag_book_3 = list(df_tag.iloc[ID_book_3][:])
    i = 0

    for tag in tag_book_1:
        if abs(tag_book_1[i] - tag_book_2[i]) <= tag_koef and abs(tag_book_2[i] - tag_book_3[i]) <= tag_koef and abs(tag_book_1[i] - tag_book_3[i]) <= tag_koef :
            if i < 3 and i > 5:
                persent_tag += 50/3
            else: persent_tag += 25/3
        i +=1


    df_d2v = pd.read_csv('D2V_results_rus.csv')
    d2v_book_1 = list(df_d2v.iloc[ID_book_1][:])
    d2v_book_2 = list(df_d2v.iloc[ID_book_2][:])
    d2v_book_3 = list(df_d2v.iloc[ID_book_3][:])
    cos_sim_12 = dot(d2v_book_1, d2v_book_2)/(norm(d2v_book_1)*norm(d2v_book_2))
    cos_sim_13 = dot(d2v_book_1, d2v_book_3)/(norm(d2v_book_1)*norm(d2v_book_3))
    cos_sim_32 = dot(d2v_book_3, d2v_book_2)/(norm(d2v_book_3)*norm(d2v_book_2))
    cos_sim = [cos_sim_12, cos_sim_13, cos_sim_32]
    if cos_sim[1] and cos_sim[0] and cos_sim[2] >= 0.5:
        koeff = max(cos_sim) - min(cos_sim) #Разница максимального с минимальным
        if koeff <= 0.4: persent_d2v = 60
        if koeff <= 0.3: persent_d2v = 70
        if koeff <= 0.2: persent_d2v = 80
        if koeff <= 0.1: persent_d2v = 90
    else:
        persent_d2v = (cos_sim[0] + cos_sim[1] + cos_sim[2])/3*0.5*100

    df_semsim = pd.read_csv('SemSim_results_rus.csv')
    sem_book_1 = list(df_semsim.iloc[ID_book_1][:])
    sem_book_2 = list(df_semsim.iloc[ID_book_2][:])
    sem_book_3 = list(df_semsim.iloc[ID_book_3][:])
    sem_sim_books = [0, 0, 0 ]
    i = 0
    for sem in sem_book_1:
        if sem_book_1[i] == sem_book_2[i]: sem_sim_books[0] += 0.2
        if sem_book_3[i] == sem_book_2[i]: sem_sim_books[1] += 0.2
        if sem_book_1[i] == sem_book_3[i]: sem_sim_books[2] += 0.2
        i +=1
    persent_semsim = min(sem_sim_books) * 10

    # ['persent_semsim', 'persent_d2v', 'persent_tag', 'persent_bow', 'persent_tfidf']
    data = {'Name': ['SemSim', 'D2V_Listed', 'Listed', 'Simil_bow' , 'sim_tfidf'], 'persent': [persent_semsim, persent_d2v, persent_tag, persent_bow, persent_tfidf]}
    accuracy_factor = pd.DataFrame(data)
    accuracy_factor['Rating_Rank'] = accuracy_factor['persent'].rank(ascending = 1)

    SemSim = accuracy_factor['Rating_Rank'][0]
    D2V_Listed = accuracy_factor['Rating_Rank'][1]
    Listed = accuracy_factor['Rating_Rank'][2]
    Simil_bow = accuracy_factor['Rating_Rank'][3]
    sim_tfidf = accuracy_factor['Rating_Rank'][4]

    cv = CountVectorizer()
    X = cv.fit_transform(df['Lemmatized']).toarray()#перевели в массив
    features = cv.get_feature_names_out()
    df_bow = pd.DataFrame(X, columns= features) #делаем мешок слов
    # df_bow.head(20)

    tfidf = TfidfVectorizer() #подбираем по частоте
    x_tfidf = tfidf.fit_transform(df['Lemmatized']).toarray()
    df_tfidf = pd.DataFrame(x_tfidf, columns = tfidf.get_feature_names_out())

    cosine_value = []
    Quest_bow = cv.transform([text_bow_book_1]).toarray()
    cosine_value_bow_1 = np.round(1 - pairwise_distances(df_bow, Quest_bow, metric= 'cosine'), 3)
    Quest_bow = cv.transform([text_bow_book_2]).toarray()
    cosine_value_bow_2 = np.round(1 - pairwise_distances(df_bow, Quest_bow, metric= 'cosine'), 3)
    Quest_bow = cv.transform([text_bow_book_3]).toarray()
    cosine_value_bow_3 = np.round(1 - pairwise_distances(df_bow, Quest_bow, metric= 'cosine'), 3)
    i = 0
    for n in cosine_value_bow_1:
        cos_bow = np.round((cosine_value_bow_1[i][0] + cosine_value_bow_2[i][0] + cosine_value_bow_3[i][0])/3 , 3)
        cosine_value.append(cos_bow)
        i+=1

    df['Simil_bow'] = cosine_value

    cos_value = []
    Quest_tfidf = tfidf.transform([text_bow_book_1]).toarray()
    cosine_value_tfidf_1 = np.round(1 - pairwise_distances(df_tfidf, Quest_tfidf, metric= 'cosine'), 3)
    Quest_tfidf = tfidf.transform([text_bow_book_2]).toarray()
    cosine_value_tfidf_2 = np.round(1 - pairwise_distances(df_tfidf, Quest_tfidf, metric= 'cosine'), 3)
    Quest_tfidf = tfidf.transform([text_bow_book_3]).toarray()
    cosine_value_tfidf_3 = np.round(1 - pairwise_distances(df_tfidf, Quest_tfidf, metric= 'cosine'), 3)
    i = 0
    for n in cosine_value_tfidf_1:
        cos_tfidf = np.round((cosine_value_tfidf_1[i][0] + cosine_value_tfidf_2[i][0] + cosine_value_tfidf_3[i][0])/3 , 3)
        cos_value.append(cos_tfidf)
        i+=1

    df['sim_tfidf'] = cos_value

    df_results = pd.DataFrame(df, columns= ['Simil_bow','sim_tfidf','SemSim','Listed', 'D2V_Listed'])

    # Создать пустой список

    df_results_list =[]
    d = []

    # Итерировать по каждой строке

    for i in range((df_results.shape[0])):

        df_results_list.append(list(df_results.iloc[i, :]))

    answer_result = df[df['title'] == title_1]
    if answer_result.empty:
       answer_result = df[df['ru_title'] == title_1]
    answer_answer_result = pd.DataFrame(answer_result, columns= ['Simil_bow','sim_tfidf','SemSim','Listed', 'D2V_Listed'])
    for i in range((answer_answer_result.shape[0])):
        d.append(list(answer_answer_result.iloc[i, :]))
    z_results = []
    for answer in d:
        for result in df_results_list:
            z = 0
            if result[0] > max(cosine_value)//3*2:
                z += Simil_bow
            if result[1] > max(cos_value)//3*2:
                z += sim_tfidf
            if result[2] == answer[2]:
                z += SemSim
            if result[3] == answer[3]:
                z += Listed
            if result[4] == answer[4]:
                z += D2V_Listed
            z_results.append(z)
    df['Z_Answer'] = pd.DataFrame(z_results)
    # cos_answer = (np.round(1 - pairwise_distances(df_results_list, answer_result, metric= 'cosine'), 2)* 100)

    import difflib
    ratio_results = []
    for results in df_results_list:


        matcher = difflib.SequenceMatcher(None, ''.join(str(answer_result)), ''.join(str(results))).ratio()
        ratio_results.append(np.round((matcher * 100),3) )

    df['Answer'] = pd.DataFrame(ratio_results)

    df_answer_sort = df.sort_values(by = 'Z_Answer', ascending= False)
    df_answer_sort_clear = df_answer_sort[df_answer_sort['title'].str.contains(title_1) == False]
    df_answer_sort_clear = df_answer_sort_clear[df_answer_sort_clear['title'].str.contains(title_2) == False]
    df_answer_sort_clear = df_answer_sort_clear[df_answer_sort_clear['title'].str.contains(title_3) == False]
    # Распечатать список
    df_answer_sort_clear.head(15)


    answer_sort = pd.DataFrame(df_answer_sort_clear, columns= ['ru_title', 'title','ru_author', 'genre'])

    # Создать пустой список

    answer_sort_list =[]


    # Итерировать по каждой строке

    for i in range((answer_sort.shape[0])):



        # Использование iloc для доступа к значениям

        # текущая строка, обозначенная "i"

        answer_sort_list.append(list(answer_sort.iloc[i, :]))
        answer_books = []
        num = 0
        for book in answer_sort_list:
            if book[0] == title_1 or book[0] == title_2 or book[0] == title_3 or book[1] == title_1 or book[1] == title_2 or book[1] == title_3:
                continue
            if num > 10: break
            else: num +=1
            answer_books.append(book[0])
    print( answer_books)

    return answer_books
