import urllib.request
import bs4


class Problem:
    def __init__(
            self,
            name: str,
            statement: str,
            timelimit: int,
            memlimit: int):
        self.__name = name
        self.__statement = statement
        self.__timelimit = timelimit
        self.__memlimit = memlimit

    @property
    def name(self) -> str:
        return self.__name

    @property
    def statement(self) -> str:
        return self.__statement

    @property
    def timelimit(self) -> int:
        return self.__timelimit

    @property
    def memlimit(self) -> int:
        return self.__memlimit

    def __str__(self):
        return '\n'.join([
            self.name,
            self.statement,
            str(self.timelimit),
            str(self.memlimit),
        ])


class Client:
    def __init__(self):
        self.__host = 'atcoder.jp'
        self.__basepath = 'contests'

    def get(self,
            contest_name: str, contest_id: str, problem_id: str) -> str:
        '''
        get [https://atcoder.jp/contests/<contest_name><contest_id>
        /tasks/<contest_name><contest_id>_<problem_name>]

        ex) contest_name = abc, contest_id = 123, problem_name = A
        -> https://atcoder.jp/abc123/abc123_a

        :param contest_name: name of contest
        :param contest_id: id of contest whose name is `contest_name`
        :param problem_name: name of problem in contest specified by 
            `contest_name` and `contest_id`
        :return: html
        '''
        url = self.__build_url(contest_name, contest_id, problem_id)
        html = self.__get_html(url)
        return self.parse(html)

    def parse(self, html: str) -> Problem:
        soup = bs4.BeautifulSoup(html, "html.parser")
        body = soup.body
        main_div = body.select('div#main-div')[0]
        main_container = main_div.select('div#main-container')[0]
        main = main_container.select('div.row > div')[1]

        problem_name = main.span.text.split(' - ')[1]

        # parse timelimit / memlimit
        limits: str = main.p.text

        t_offset = limits.index('Time Limit:')
        t_end = limits.index('sec')
        timelimit = int(limits[t_offset+len('Time Limit:'):t_end])

        m_offset = limits.index('Memory Limit:')
        m_end = limits.index('MB')
        memlimit = int(limits[m_offset+len('Memory Limit:'):m_end])

        return Problem(
            name=problem_name,
            statement='',
            timelimit=timelimit,
            memlimit=memlimit)

    def __get_html(self, url: str) -> str:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        return body.decode('utf-8')

    def __build_url(self, contest: str, _id: str, problem: str) -> str:
        url = 'https://{host}/contests/{contest}/tasks/{contest}_{problem}' \
            .format(host=self.__host, contest=contest+_id, problem=problem)
        return url + '?lang=en'
