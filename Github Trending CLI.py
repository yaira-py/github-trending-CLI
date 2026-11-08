import argparse,json,ssl,urllib.request,urllib.parse
from datetime import datetime,timedelta

ctx =ssl._create_unverified_context()

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req,context=ctx , timeout=20).read())


def main():
   p=argparse.ArgumentParser(description='Github Trending CLI')
   p.add_argument('--language',default='', help='e.g. python,javascript, rust')
   p.add_argument('--days',type=int, default=7,help='trending in last N days')
   p.add_argument('--limit',type=int, default=10, help='how many repos to show')
   args=p.parse_args()

   since=(datetime.now()- timedelta(days=args.days)).strftime('%Y-%m-%d')
   q=f'created:>{since} stars:>100'
   if args.language:
       q+= f'language: {args.language}'

   url= 'https://api.github.com/search/repositories?q=' + urllib.parse.quote(q)
   data= fetch(url)

   print(f'\n🔥 Github Trending - last {args.days} days ')
   print('-'*80)

   for i,repo in enumerate(data['items'],1):
       print(f'{i}. {repo['full_name']} ⭐️ {repo['stargazers_count']}')
       print(f' {repo["description"] or "No description" }')
       print(f' {repo['html_url']} | Lang: {repo['language']} | Forks: {repo['forks_count']}')
       print()





if __name__=='__main__':
    main()
