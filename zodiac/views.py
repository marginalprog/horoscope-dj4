from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


def main_page(request):
    return HttpResponse("Главная страница")


dict_zodiac = {
    'aries': 'Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).',
    'taurus': 'Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).',
    'gemini': 'Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).',
    'cancer': 'Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).',
    'leo': ' Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).',
    'virgo': 'Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).',
    'libra': 'Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).',
    'scorpio': 'Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).',
    'sagittarius': 'Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).',
    'capricorn': 'Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).',
    'aquarius': 'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).',
    'pisces': 'Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта).',
}

dict_types_zodiac = {
    'air': ['gemini', 'libra', 'aquarius'],
    'earth': ['taurus', 'virgo', 'capricorn'],
    'fire': ['aries', 'leo', 'sagittarius'],
    'water': ['cancer', 'scorpio', 'pisces'],
}

dict_dates_zodiac = {
    'capricorn': [1, 20],
    'aquarius': [21, 50],
    'pisces': [51, 79],
    'aries': [80, 110],
    'taurus': [111, 141],
    'gemini':  [142, 172],
    'cancer': [173, 203],
    'leo': [204, 233],
    'virgo': [234, 266],
    'libra': [267, 296],
    'scorpio': [297, 326],
    'sagittarius': [327, 356],
    # если ничего не нашли, значит знак козерог (тк >357 и <366)
}


dict_month_days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def index(request):
    list_sign_zodiac = list(dict_zodiac)
    """
    <ol>
      <li>aries</li>
      <li>taurus</li>
      <li>aries</li>
    </ol>
    """
    list_elements = ""
    for sign in list_sign_zodiac:
        redirect_path = reverse("horoscope_name", args=(sign,))
        list_elements += f"<li><a href='{redirect_path}'>{sign.title()}</a></li>"
    response = f"<ol>{list_elements}</ol>"
    return HttpResponse(response)


def get_all_types(request):
    list_type_zodiac = list(dict_types_zodiac)
    list_elements = ""
    for ztype in list_type_zodiac:
        redirect_path = reverse("type_name", args=(ztype,))
        list_elements += f"<li><a href='{redirect_path}'>{ztype.title()}</a></li>"
    response = f"<ol>{list_elements}</ol>"
    return HttpResponse(response)


def get_info_about_type(request, type_zodiac):
    list_signs_zodiac = dict_types_zodiac[type_zodiac]
    list_elements = ""
    for sign in list_signs_zodiac:
        redirect_path = reverse("type_name", args=(sign,))
        list_elements += f"<li><a href='{redirect_path}'>{sign.title()}</a></li>"
    response = f"<ol>{list_elements}</ol>"
    return HttpResponse(response)


def get_info_about_sign_zodiac(request, sign_zodiac: str):
    """
    Получает на вход переданный параметр из urls и определяет возврат http-ответ.
    Использование данного вида представления даёт возможность избавиться от избыточности
    (повторений и т.п.) в коде файла views. Всё уместится в одну функцию.
    request: запрос
    sign_zodiac: выбранный пользователем знак зодиака
    """
    if dict_zodiac.get(sign_zodiac, None):
        return HttpResponse(f'<h2>{dict_zodiac.get(sign_zodiac)}</h2>')
    else:
        return HttpResponseNotFound(f"{sign_zodiac} - неизвестный знак зодиака")


def get_info_about_sign_zodiac_number(request, sign_zodiac: int):
    """
    Аналогичное представление, но принимающее на вход число.
    Создано для демонстрации работы конвертеров роутов,
    а также для демонстрации Redirect URLs (перенаправлений)
    request: запрос
    sign_zodiac: выбранный пользователем знак зодиака
    """
    list_sign_zodiac = list(dict_zodiac)
    if sign_zodiac > len(list_sign_zodiac):
        return HttpResponseNotFound(f"Передан неправильный номер знака зодиака {sign_zodiac}")
    name_zodiac = list_sign_zodiac[sign_zodiac - 1]
    redirect_url = reverse("horoscope_name", args=(name_zodiac,))
    return HttpResponseRedirect(redirect_url)


def get_info_by_day(request, month, day):
    """
    Представление получает на вход месяц и день, по которому определяет знак зодиака и
    перенаправляет запрос на информацию о данном знаке зодиака
    """
    insert_days = 0
    for k, v in dict_month_days.items():
        if k == month:
            break
        insert_days += v  # суммируем кол-во дней по порядку, пока не дойдем до введённого месяца
    insert_days += day  # добавляем к вычисленной сумме день, который был введён

    list_sign_zodiac = list(dict_dates_zodiac)
    for sign, days in dict_dates_zodiac.items():
        if insert_days in range(days[0], days[1]):
            redirect_url = reverse("horoscope_name", args=(sign,))
            return HttpResponseRedirect(redirect_url)
    if insert_days < 366:  # Если не нашли в словаре знак зодиака, но день <366 - это capricorn
        name_zodiac = list_sign_zodiac[0]
        redirect_url = reverse("horoscope_name", args=(name_zodiac,))
        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponse(f"Введена некорректная дата: {month} месяц, {day} день")
