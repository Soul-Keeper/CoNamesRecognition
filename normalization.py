import re
#import cld3
from camel_tools.utils.charmap import CharMapper
from cleanco import basename
from transliterate import translit


class Normalizer:

    def __init__(self):

        """
        """

        self.replace_list = [
            "co.",
            " co ",
            " co",
            "co ",
            "ltd.",
            ",",
            "plc.",
            " plc ",
            " plc",
            "plc ",
            "s. de r.l.",
            "s.r.l.",
            "s.r.l",
            "s r l",
            " srl ",
            "srl ",
            " srl",
            "s.a.u.",
            "s.a.u",
            "s a u",
            " sau ",
            "sau ",
            " sau",
            "s.p.a.",
            "s.p.a",
            "s p a",
            " spa ",
            "spa ",
            " spa",
            "s.l.u.",
            "s.l.u",
            "s l u",
            " slu ",
            " slu",
            "slu ",
            "s.a.",
            "s a",
            " sa ",
            "sa ",
            " sa",
            "s.l.",
            "s l",
            " sl ",
            " sl",
            "sl ",
            " sarl ",
            " sarl",
            "sarl ",
            "ооо",
            " зао ",
            "зао ",
            " зао",
            " оао ",
            "оао ",
            " оао",
            "общество с ограниченной ответственностью",
            " ао ",
            "ао ",
            " ао",
            "а о",
            "акционерное общество",
            " oü ",
            " oü",
            "oü ",
            " ulc ",
            " ulc",
            "ulc ",
            "san.",
            "ti̇c.",
            "san. ve tic.",
            "a.s.",
            "a s",
            "a/s",
            "as",
            "sp.",
            "z o o",
            "o.o.",
            "o o",
            " z ",
            "e c.",
            "e c",
            "m.b.h.",
            "m.b.h",
            "m b h",
            " mbh ",
            " mbh",
            "mbh ",
            "a.g.",
            "a.g",
            " ag ",
            " ag",
            "ag ",
            "a g",
            "gmbh",
            "n.v.",
            "n.v",
            " nv ",
            "nv ",
            " nv",
            "n v",
            "b.v.",
            "b.v",
            " bv ",
            "b v",
            " de ",
            " de",
            "de ",
            "pvt.",
            " pvt ",
            "pvt ",
            " pvt",
            "mfg.",
            " mfg ",
            " mfg",
            "mfg ",
            "inc.",
            " inc ",
            " inc",
            "inc ",
            "corp.",
            " corp ",
            " corp",
            "corp ",
            "imp.",
            "exp.",
        ]
        
    def normalize(self, string_value: str) -> str:

        """
        Normalize company name
        return normalized str

        * to add new words to replace_list use .add_to_replace_list

        string_value: str - string for normalizing
        """

        normalized_name = string_value
        replace = self.replace_list

        if normalized_name is None or normalized_name == "":
            return "Error"

        # убираем лишние пробелы у скобок
        normalized_name = re.sub("\s\(\s", " (", normalized_name)
        normalized_name = re.sub("\s\)\s", ") ", normalized_name)

        # удаляем все скобки
        normalized_name = re.sub("\(.*?\)", "", normalized_name)

        # переводим в нижний регистр
        normalized_name = normalized_name.lower()

        for item in replace:
            normalized_name = normalized_name.replace(item, " ")

        # убираем знаки, стоящие отдельно
        normalized_name = re.sub("\s[\.&:\*\"'\`]+\s", " ", normalized_name)
        normalized_name = re.sub("\s[\.&:\*\"'\`]+$", "", normalized_name)
        normalized_name = re.sub("^[\.&:\*\"'\`]+\s", "", normalized_name)

        # убираем лишние пробелы у дефисов
        normalized_name = re.sub("-\s", "-", normalized_name)
        normalized_name = re.sub("\s-", "-", normalized_name)
        normalized_name = re.sub("[\"'\`]+", " ", normalized_name)

        # убираем лишние пробелы
        normalized_name = basename(normalized_name)

        if normalized_name is None or normalized_name == "":
            return "Error"

        try:
            name_language = cld3.get_language(normalized_name).language
            if name_language == "ar":
                normalized_name = CharMapper.builtin_mapper(normalized_name)
            elif name_language == "ru" or "sr" or "ka" or "bg" or "hy" or "el":
                normalized_name = translit(normalized_name, reversed=True)
        except:
            pass

        return normalized_name

    def add_to_replace_list(self, add_replace: list):

        """
        Allow add words to replace_list
        """

        self.replace_list += add_replace
        print("Added")
