import re
import traceback


def instructions():
    """ Simple instructions for default page access """

    instructions_text = 'Here is how to use this calculator:<br>'
    instructions_text += 'http://localhost:8080/ => These instructions<br>'
    instructions_text += 'To add:  http://localhost:8080/add/23/42 => 65<br>'
    instructions_text += 'To subtract:  http://localhost:8080/subtract/23/42 => -19<br>'
    instructions_text += 'To multiply:  http://localhost:8080/multiply/3/5 => 15<br>'
    instructions_text += 'To divide:  http://localhost:8080/divide/22/11 => 2'

    return instructions_text


def add(*args):
    """ Returns a string with the arguments added """

    result = int(args[0]) + int(args[1])

    return str(result)


def subtract(*args):
    """ Returns a string with the arguments subtracted """

    result = int(args[0]) - int(args[1])

    return str(result)


def multiply(*args):
    """ Returns a string with the arguments multiplied """

    result = int(args[0]) * int(args[1])

    return str(result)


def divide(*args):
    """ Returns a string with the arguments divided """

    if args[1] == "0":
        result = 'Division by zero is not allowed!'
    else:
        result = int(args[0]) / int(args[1])

    return str(result)


def resolve_path(path):
    """ Should return two values: a callable and an iterable of arguments """

    funcs = {
        '': instructions,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    """ Receive client request and act accordingly """

    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        func, args = resolve_path(path)
        status = "200 OK"
        body = func(*args)
    except NameError:
        status = '404 Not Found'
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
