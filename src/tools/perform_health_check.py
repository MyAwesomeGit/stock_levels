from fastapi import statusfrom fastapi.responses import JSONResponsefrom src.tools.connection_creator import ConnectionCreatorfrom stock_levels_logging import stock_levels_loggingdef perform_health_check():    conn = ConnectionCreator.create_connection()    with conn:        cur = conn.cursor()        cur.execute("SELECT current_database();")        health_check = cur.fetchone()[0]        stock_levels_logging.info(health_check)        return JSONResponse(            status_code=status.HTTP_200_OK,            content={                "health_check": health_check            }        )