import requests
import csv
from lxml import html
import re
MOVIE_LIST_FILE="csv_data/movie_list.csv"
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL_1="https://www.themoviedb.org/movie/"#高分电影榜单(第一页)
TMDB_TOP_URL_2="https://www.themoviedb.org/discover/movie/items"#高分电影榜单的url(第二页之后)


def get_movie_year(movie_years):
    movie_year=movie_years[0].strip() if movie_years else ''
    return movie_year.replace("(","").replace(")","")


def get_movie_publish_date(movie_dates):
    movie_date=movie_dates[0].strip() if movie_dates else ''
    return re.search(r"\d{4}-\d{2}-\d{2}",movie_date).group()
def get_movie_cost_time(movie_cost_times):
    movie_cost_time=movie_cost_times[0].strip() if movie_cost_times else ''
    h_res=re.search(r"(\d+)h",movie_cost_time)
    m_res=re.search(r"(\d+)m",movie_cost_time)
    h=int(h_res.group(1)) if h_res else 0
    m=int(m_res.group(1)) if m_res else 0
    return h*60+m

def get_movie_url(movie_info_url):
    headers = {"Accept-Language": "zh-CN,zh;q=0.9"}

    movie_response=requests.get(movie_info_url,timeout=20,headers=headers)

    movie_doc=html.fromstring(movie_response.text)
    movie_name=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    movie_years=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    movie_dates=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")
    movie_tags=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")
    movie_cost_times=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")
    movie_scores=movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    movie_languages=movie_doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    movie_directors=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_authors=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogans=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")
    movie_descriptions=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")
    movie_info={
        "电影名":movie_name[0].strip() if movie_name else '',
        "年份":get_movie_year(movie_years),
        "上映时间":get_movie_publish_date(movie_dates),
        "类型":",".join(movie_tags) if movie_tags else '',
        "评分":movie_scores[0].strip() if movie_scores else '',
        "时长":get_movie_cost_time(movie_cost_times),
        "语言":movie_languages[0].strip() if movie_languages else '',
        "导演":",".join(movie_directors) if movie_directors else '',
        "作者":",".join(movie_authors) if movie_authors else '',
        "宣传语":movie_slogans[0].strip() if movie_slogans else '',
        "简介":movie_descriptions[0].strip() if movie_descriptions else '',
    }
    print(movie_info)
    return movie_info


def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE,'w',encoding="utf-8",newline="") as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["电影名","年份","上映时间","类型","时长","评分","语言","导演","作者","宣传语","简介"])
        writer.writeheader()
        writer.writerows(all_movies)


def main():
    #循环获取电影列表（第一页到第五页）
 all_movies = []
    #1.发送请求，获取电影详情数据
 for page_num in range(1,6):
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_1, timeout=60)

        else:
            response = requests.post(TMDB_TOP_URL_2,f"air_date.gte=&air_date.lte=&certification=&certification_country=MO&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-15&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=MO&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400",
 timeout=60)

        print(f"发送请求,访问第{page_num}页数据，获取TMDB电影榜单")
    #2.解析数据，获取电影详情
        document = html.fromstring(response.content)
        movie_list=document.xpath("//div[@class='media-list-results contents']/div")
        for movie in movie_list:
           movie_urls=movie.xpath("./div/div/a/@href")
           if movie_urls:
            #电影详情的url
              movie_info_url=TMDB_BASE_URL+movie_urls[0]
            #发送请求，获取电影详情数据
              print(f"发送请求{movie_info_url}")
              movie_info=get_movie_url(movie_info_url)
              all_movies.append(movie_info)
    #3.返回电影详情：字典
        print("获取到所有电影详情，保存电影数据到csv文件...")
        save_all_movies(all_movies)
if __name__=="__main__":
    main()