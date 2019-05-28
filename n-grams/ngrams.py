import psycopg2
import sys
from pandas import DataFrame

def extractNGrams(con, query, obj, grams, count, name):
    cur = con.cursor(name)
    cur.execute(query)
    iters = 0
    for comment in cur:
        if(comment[0] != None):
            words = comment[0].split(' ')
            for i in range(len(words) - count - len(grams)):
                valid = True
                for j in range(len(grams)):
                    if(words[i+j].lower() != grams[j]):
                        valid = False
                if(valid == True):
                    concat = ' '.join(words[i+len(grams):i+len(grams)+count]).lower()
                    if(obj.get(concat) == None):
                        obj[concat] = 1
                    else:
                        obj[concat] += 1
        iters += 1
        if(iters % 10000 == 0):
            print("  Processed " + str(iters))
            
def save(obj, grams, count):
    words = []
    nums = []
    
    for word, num in obj.items():
        words.append(word)
        nums.append(num)
        
    data = {
      'followup': words,
      'count': nums
    }
    
    savePath = '_'.join(grams) + '_' + str(count) + '.csv'
    
    df = DataFrame(data, columns=['followup', 'count'])
    df.to_csv(savePath, index=None, header=True)

grams = sys.argv[1:-1]
count = int(sys.argv[-1])

con = psycopg2.connect(host = 'localhost',
                       database = 'redditModerated',
                       user = 'postgres',
                       password = '')

obj = {}

print("Fetching submissions")
extractNGrams(con, "SELECT selftext FROM Submissions", obj, grams, count, 'cur1')

print("Fetching Comments")
extractNGrams(con, "SELECT body FROM Comments", obj, grams, count, 'cur2')

print("Saving")
save(obj, grams, count)


                    