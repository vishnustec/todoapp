from todoapp.models import users,todos


session={}


def logrqd(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("You must login")
    return wrapper

# Authentication
def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user_data=[user for user in users if user["username"]==username and user["password"]==password]
    return user_data

print(authenticate(username="akhil",password="Password@123"))


# User signin
class Signin:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print("success")
        else:
            print("Invalid login")

    def logout(*args,**kwargs):
        session.pop("user")


# list all tasks and add new task
class Todo:
    @logrqd

    def get(self,*args,**kwargs):
        return todos

    def post(self,*args,**kwargs):
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        todos.append(kwargs)
        print("New task added")
        print(todos)

class TodoList:
    def get(self,*args,**kwargs):
        userId=session["user"]["id"]
        print(userId)
        list=[todo for todo in todos if todo["userId"]==userId]
        return list


class TodoDetail:
    def get_object(self,id):
        t_data=[todo for todo in todos if todo["todoId"]==id]
        return t_data


    def get(self,*args,**kwargs):
        t_id=kwargs.get("t_id")
        t_data=self.get_object(t_id)
        return t_data



    def delete(self,*args,**kwargs):
        t_id=kwargs.get("t_id")
        t_data=self.get_object(t_id)
        if t_data:
            data=t_data[0]
            todos.remove(data)
            print("Task Removed")
            print(len(todos))


    def put(self,*args,**kwargs):
        t_id=kwargs.get("t_id")
        t_data=kwargs.get("t_data")
        data=self.get_object(t_id)
        if data:
            t_obj=data[0]
            t_obj.update(t_data)
            return t_obj



# signin
sign=Signin()
sign.post(username="akhil",password="Password@123")
print(session)

#list task Add new task
todo=Todo()
print(todo.get())
todo.post(todoId=9,taskname="foodbill",status=True)

# Display logged user tasks
tlist=TodoList()
print(tlist.get())

#Delete task
t_detail=TodoDetail()
t_detail.delete(t_id=7)

# To get specific task details
print(t_detail.get(t_id=2))

#Task update

t_data={
"task_name":"electricity bill"
}

t_detail=TodoDetail()
print(t_detail.put(t_id=3,t_data=t_data))