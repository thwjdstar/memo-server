from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector import Error
from mysql_connection import get_connection

class MemoListResource(Resource) :
    @jwt_required() 
    def post(self) :

        data = request.get_json()
        userId = get_jwt_identity()
        
        print(data)

        try :
            connection = get_connection()

            query = '''insert into memo
                    (userId,title, date, content)
                    values
                    (%s,%s,%s,%s);'''
        
            record = (userId,
                    data['title'],
                    data['date'],
                    data['content'])
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
        
            return {"result": "fail","error" : str(e)}, 500
    
        return {"result" : "success"}, 200

class MemoResource(Resource) :        
    @jwt_required()
    def put(self,memo_id) :

        
            data = request.get_json()
            userId = get_jwt_identity()

            
            try :
                connection = get_connection()

                query = '''update memo
                            set title = %s,
                            date = %s,
                            content = %s,
                            where id= %s and userId =%s;'''
                
                record = (data['title'],
                          data['date'],
                          data['content'],
                          memo_id,
                          userId)
                
                cursor = connection.cursor()
                cursor.execute(query, record)
                connection.commit()

                cursor.close()
                connection.close()

            except Error as e :
                print(e)
                cursor.close()
                connection.close()
                return{'result' : 'fail','error':str(e)}, 500            

            
            return {'result' : 'success'}, 200 
    