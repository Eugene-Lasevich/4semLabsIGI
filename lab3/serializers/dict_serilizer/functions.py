import re
from pydoc import locate
import inspect
import types


# from constants import *


def serealize(obj):
    if (isinstance(obj, (int, bool, str, float, type(None), complex))):
        obj = serealize_single(obj)
    elif (isinstance(obj, (list, tuple, set, frozenset, bytes))):
        obj = serealize_list(obj)
    elif (isinstance(obj, dict)):
        obj = serealize_dict(obj)
    elif (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, types.LambdaType)):
        obj = serealize_func(obj)
    elif (inspect.iscode(obj)):
        obj = serealize_code(obj)
    elif (inspect.isclass(obj)):
        obj = ser_class_old(obj)
    elif (inspect.ismethoddescriptor(obj) or inspect.isbuiltin(obj)):
        obj = serealize_instance(obj)
    elif inspect.ismemberdescriptor(obj):
        obj = serealize_instance(obj)
    elif inspect.isgetsetdescriptor(obj):
        obj = serealize_instance(obj)
    elif isinstance(obj, type(type.__dict__)):
        obj = serealize_instance(obj)
    elif inspect.ismodule(obj):
        return serealize_module(obj)

    else:
        obj = serealize_object(obj)

    # obj = tuple((k, obj[k]) for k in obj)

    return obj


def serealize_single(obj):
    serealized = dict()
    serealized['type'] = re.findall('\'\w+\'', str(type(obj)))[0].replace('\'', '')
    serealized['value'] = obj

    return serealized


def serealize_list(obj):
    serealized = dict()
    serealized['type'] = re.findall('\'\w+\'', str(type(obj)))[0].replace('\'', '')
    serealized['value'] = [serealize(tmp) for tmp in obj]

    return serealized


def serealize_dict(obj):
    serealized = dict()
    serealized['type'] = 'dict'
    serealized['value'] = dict()
    # serealized['value'] = tuple([tuple([serealize(obj[i]), serealize(i)]) for i in obj])

    serealized['value'] = [[serealize(tmp), serealize(obj[tmp])] for tmp in obj]

    return serealized


def serealize_func(obj):
    mems = inspect.getmembers(obj)
    serealized = dict()
    serealized['type'] = str(type(obj))[8:-2]
    val = dict()

    for tmp in mems:
        if (tmp[0] in ['__code__', '__name__', '__defaults__']):
            val[tmp[0]] = (tmp[1])
        if tmp[0] == '__code__':
            co_names = tmp[1].__getattribute__('co_names')
            globs = obj.__getattribute__('__globals__')
            val['__globals__'] = dict()

            for tmp_co_names in co_names:
                if tmp_co_names == obj.__name__:
                    val['__globals__'][tmp_co_names] = obj.__name__
                elif not inspect.ismodule(tmp_co_names) \
                        and tmp_co_names in globs:
                    # and tmp_co_names not in __builtins__:
                    val['__globals__'][tmp_co_names] = globs[tmp_co_names]

    serealized['value'] = serealize(val)

    return serealized


def serealize_code(obj):
    if (str(type(obj))[8:-2] == 'NoneType'):
        return None

    mems = inspect.getmembers(obj)

    serealized = dict()
    serealized['type'] = str(type(obj))[8:-2]
    serealized['value'] = serealize({tmp[0]: tmp[1] for tmp in mems if not callable(tmp[1])})

    return serealized


def serealize_instance(obj):
    mems = inspect.getmembers(obj)

    serealized = dict()
    serealized['type'] = str(type(obj))[8:-2]
    serealized['value'] = serealize({tmp[0]: tmp[1] for tmp in mems if not callable(tmp[1])})

    return serealized


def ser_class_old(obj):
    serealized = dict()
    val = dict()

    serealized['type'] = 'class'
    val['__name__'] = obj.__name__
    members = inspect.getmembers(obj)

    for tmp in members:
        if tmp[0] not in ['__class__',
                          '__getattribute__',
                          '__new__',
                          '__setattr__']:
            val[tmp[0]] = tmp[1]
    serealized['value'] = serealize(val)

    return serealized




def serealize_object(obj):
    serealized = dict()
    serealized['type'] = 'object'
    serealized['value'] = serealize({'__object_type__': type(obj), '__fields__': obj.__dict__})

    # for key, value in inspect.getmembers(obj):
    #    if not key.startwith('__') and not inspect.isfunction(value):
    #        serealized['__fields__'][key] = serealize(value)

    return serealized


def serealize_module(obj):
    tmp = str(obj)
    serealized = {'type': types.get_type(obj), 'value': tmp[9:-13]}

    return serealized


def deseralize(obj):
    if (obj['type'] in ['int', 'float', 'bool', 'complex', 'str']):
        return deserealize_single(obj)
    if (obj['type'] in ['list', 'set', 'frozenset', 'tuple', 'bytes']):
        return deserealize_list(obj)
    if (obj['type'] == 'dict'):
        return deserealize_dict(obj)
    if (obj['type'] == 'object'):
        return deserealize_object(obj)
    if (obj['type'] == 'class'):
        return deserealize_class(obj)
    if (obj['type'] == 'function'):
        return deserealize_func(obj)
    if (obj['type'] == 'module'):
        return deseralize_module(obj)


def deserealize_single(obj):
    tmp_obj = locate(obj['type'])
    return tmp_obj(obj['value'])


def deserealize_list(obj):
    tmp_obj = locate(obj['type'])
    return tmp_obj([deseralize(tmp) for tmp in obj['value']])


def deserealize_dict(obj):
    return {deseralize(tmp[0]): deseralize(tmp[1]) for tmp in obj['value']}


def deserealize_object(obj):
    value = deseralize(obj['value'])
    result = value['__object_type__'](**value['__fields__'])

    for key, value in value['__fields__'].items():
        result.key = value

    return result



def deserealize_class(obj):
    class_dict = deseralize(obj['value'])
    name = class_dict['__name__']
    del class_dict['__name__']

    return type(name, (object,), class_dict)


code_args = [
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_linetable',
    'co_freevars',
    'co_cellvars'
]


def deserealize_code(obj):
    objs = obj['value']['value']

    for tmp in objs:
        if tmp[0]['value'] == '__code__':
            args = deseralize(tmp[1]['value'])
            code_dict = dict()
            for arg in args:
                arg_val = args[arg]
                if arg != '__doc__':
                    code_dict[arg] = arg_val
            code_list = [0] * 16

            for name in code_dict:
                if (name == 'co_lnotab'):
                    continue
                code_list[code_args.index(name)] = code_dict[name]

            return types.CodeType(*code_list)


def deserealize_func(obj):
    res_dict = deseralize(obj['value'])
    res_dict['code'] = deserealize_code(obj)
    res_dict.pop('__code__')
    res_dict['globals'] = res_dict['__globals__']
    res_dict.pop('__globals__')
    res_dict['name'] = res_dict['__name__']
    res_dict.pop('__name__')
    res_dict['argdefs'] = res_dict['__defaults__']
    res_dict.pop('__defaults__')

    res = types.FunctionType(**res_dict)
    if res.__name__ in res.__getattribute__('__globals__'):
        res.__getattribute__('__globals__')[res.__name__] = res

    return res


def deseralize_module(obj):
    return __import__(obj['value'])


