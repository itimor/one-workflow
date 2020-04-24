# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.views import exception_handler
from common import status


def JSONExceptionHandler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        resp = {
            'code': status.HTTP_400_BAD_REQUEST,
            'result': dict(response.data)
        }
        response.data = resp

    return response


class ExceptionX_Result:
    exceptionType = None
    exceptionTitle = None
    exceptionDetail = None


class ExceptionX:

    @staticmethod
    def ToString(e):
        result = ExceptionX_Result
        tempStr = str(type(e))
        tempStrArray = tempStr.split("'")
        result.exceptionTitle = tempStrArray[1]
        result.exceptionType = tempStrArray[0][1:]
        result.exceptionDetail = str(e)

        if result.exceptionDetail[0] == "<":
            if result.exceptionDetail[result.exceptionDetail.__len__() - 1] == ">":
                result.exceptionDetail = result.exceptionDetail[1:result.exceptionDetail.__len__() - 1]
        return result

    @staticmethod
    def PasreRaise(e):
        result = ExceptionX_Result
        tempStr = str(type(e))
        tempStrArray = tempStr.split("'")
        result.exceptionTitle = tempStrArray[1]
        result.exceptionType = tempStrArray[0][1:]
        result.exceptionDetail = str(e)

        if result.exceptionDetail[0] == "<":
            if result.exceptionDetail[result.exceptionDetail.__len__() - 1] == ">":
                result.exceptionDetail = result.exceptionDetail[1:result.exceptionDetail.__len__() - 1]
        return result.exceptionDetail
