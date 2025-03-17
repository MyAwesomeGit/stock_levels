import loggingimport uvicornfrom fastapi import FastAPI, Response, status, Request, HTTPExceptionfrom fastapi.responses import JSONResponsefrom pydantic import ValidationErrorimport requestsfrom src.model.input_data import InputDatafrom src.model.stock_levels_messages import StockLevelsMessagesfrom src.tools.perform_health_check import perform_health_checkapp = FastAPI()@app.on_event("startup")def startup():    logging.info("App started.")@app.get("/health_check")def health_check():    health_check_result = perform_health_check()    return health_check_result@app.get("/stock")async def get_stock_quantity(request: Request):    try:        body = await request.body()        if not body:            response = Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,                                content="perform_if_not_body")            return response        received_request_content = await request.json()        input_data = InputData(**received_request_content)        logging.info(f"input_data: {input_data}")        response = JSONResponse(            status_code=status.HTTP_200_OK,            content={"message": "app_received_input_parameters",                     "data": input_data.dict()}        )        return response    except ValidationError as e:        errors = e.errors()        simplified_errors = []        for error in errors:            simplified_errors.append({                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,                "msg": StockLevelsMessages.missing_field_value,                "field": error.get("loc")[0]            })        return JSONResponse(            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,            content={"errors": simplified_errors}        )    except ValueError as e:        return HTTPException(            status_code=status.HTTP_400_BAD_REQUEST,            detail=str(e),        )    except Exception as e:        return HTTPException(            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,            detail=str(e),        )if __name__ == '__main__':    uvicorn.run("main:app")