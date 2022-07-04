from todosapplica.modeltodo import users,todos

def authenticate(*args,**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    userdata=[user for user in users if user["username"]==username]
    return userdata

# authenticate(username="anu",password="Password@123")

session={}

def login_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you must login")
    return wrapper



class SignInView:

    def __init__(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            print("success")
            session["user"]=user[0]
        else:
            print("invalid credentials")

class ListAllTodos:
    @login_required
    def get(self,*args,**kwargs):
        return todos

class CreateTodo:
    @login_required
    def post(self,*args,**kwargs):
        todoId=kwargs.get("todoId")
        user_id=session["user"]["id"]
        task_name=kwargs.get("task_name")
        completed=kwargs.get("completed")
        data={
              "todoId":todoId,
             "userId":user_id,
              "task_name":task_name,
              "completed":completed
        }
        todos.append(data)
        print("created a todo successfully")
        print(todos[-1])

class MyTodos:
    @login_required
    def get(self,*args,**kwargs):
        user_id=session["user"]["id"]
        mytodo=[todo for todo in todos if todo["userId"]==user_id]
        print("My Todos :" ,mytodo)

class TodoChanges:
    @login_required
    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo

    def put(self,*args,**kwargs):
        todoId=kwargs.get("todoId")
        data=self.get_object(todoId)
        update = kwargs.get("update")
        if data:
            todo=data[0]
            todo.update(update)
            print("updated the todo status")
            print(todo)


    def delete(self,*args,**kwargs):
        todoId=kwargs.get("todoId")
        data=self.get_object(todoId)
        if data:
            todo=data[0]
            todos.remove(todo)
            print("deleted the todo successfully")
            print(todos)
@login_required
def signout():
    user=session.pop("user")
    username = user["username"]
    print(f"user {username} has been logged out")



log=SignInView(username="anu",password="Password@123")
# print(session)
all_todos=ListAllTodos()
print("All Todos :",all_todos.get())
specific_todo=all_todos.get()
for todo in specific_todo:
    if todo["todoId"]== 7:
        print("Checking Todo of todoId",todo["todoId"],":", todo)
create=CreateTodo()
create.post(todoId=9,task_name="credbill",completed="True")
my_todos=MyTodos()
my_todos.get()
changes_todo=TodoChanges()
update={"completed":"True"}
changes_todo.put(todoId=5,update=update)
changes_todo.delete(todoId=6)
signout()



