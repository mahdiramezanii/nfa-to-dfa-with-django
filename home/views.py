from django.shortcuts import render,HttpResponse
from .models import counter,result
import pandas as pd

def home(request):

    context = {
        "numbers":range(0),
        "numbers2":range(0),
        "value1":0,
        "value2":0,
        "status_set_value":True,
        "status_convert":False,
        "status_final":False,
        "show_respons":False
    }

    nfa={}
    nfa_final_state=""
    if request.method=="POST":
        n=request.POST.get("n")
        t=request.POST.get("t")

        context["status_convert"]=True
        context["status_set_value"]=False


        if n and t:


            counter.objects.create(n=n,t=t,recahng=0)

            context["numbers"]=range(int(n))
            context["numbers2"]=range(int(t))
            context["value1"]=int(n)
            context["value2"]=int(t)

    # ===== crete data from database =========

    numbers = counter.objects.all().last()
    new_n = numbers.n
    new_t = numbers.t
    new_z=numbers.recahng

    # ======== End database ========

    if request.method=="POST":

        for i in range(new_n):
            state=request.POST.getlist("state")

            if state:
                nfa[state[i]]={}
                for j in range(new_t):
                    path=request.POST.getlist("path")
                    reaching_state=request.POST.getlist("reaching_state")
                    newreaching_state=[]

                    print("reaching_state")

                    for item in reaching_state:

                        if item != " ":
                            newreaching_state.append(item.split())

                        print(newreaching_state)

                    if path and newreaching_state:



                        for z in range(numbers.recahng,(new_t*2)):

                            nfa[state[i]][path[j]] = newreaching_state[z]
                            break
                    numbers.recahng=numbers.recahng+1
                    numbers.save()

                context["status_convert"] = False
                context["status_final"] = True

    print(nfa)
    nfa_table = pd.DataFrame(nfa)
    print(nfa_table.transpose())

    """if len(nfa)>0:
        result_data=result.objects.create(nfa_nfa=nfa,nfa_pandas=nfa_table)

        #context["response_nfa_nfa"]=result_data.nfa_nfa.all()

    context["response_nfa_pandas"]=result.objects.all().last()"""

    if request.method=="POST":
        nfa_final=request.POST.get("final")

        if nfa_final:
            nfa_final_state = [x for x in nfa_final.split()]

            context["show_respons"]=True

    new_states_list = []
    dfa = {}

    if nfa.keys():

            keys_list = list(list(nfa.keys())[0])
            path_list = list(nfa[keys_list[0]].keys())

            dfa[keys_list[0]] = {}
            for y in range(new_t):
                var = "".join(nfa[keys_list[0]][path_list[y]])
                dfa[keys_list[0]][path_list[y]] = var
                if var not in keys_list:
                    new_states_list.append(var)
                    keys_list.append(var)

            while len(new_states_list) != 0:
                dfa[new_states_list[0]] = {}

                for _ in range(len(new_states_list[0])):

                    for i in range(len(path_list)):
                        temp = []

                        for j in range(len(new_states_list[0])):
                            temp += nfa[new_states_list[0][j]][path_list[i]]

                        s = ""
                        s = s.join(temp)

                        if s not in keys_list:
                            new_states_list.append(s)
                            keys_list.append(s)

                        dfa[new_states_list[0]][path_list[i]] = s

                new_states_list.remove(new_states_list[0])

            print("\nDFA :- \n")
            print(dfa)
            print("\nPrinting DFA table :- ")
            dfa_table = pd.DataFrame(dfa)
            print(dfa_table.transpose())
            """geeks_object=dfa_table.to_html()"""

            if len(dfa)>0:
                result_data = result.objects.create(nfa_nfa=nfa, nfa_pandas=nfa_table,dfa_dfa=dfa,dfa_pandas=dfa_table)

            dfa_states_list = list(dfa.keys())
            dfa_final_states = []
            for x in dfa_states_list:
                if nfa_final_state:
                    for i in x:
                        if i in nfa_final_state:
                            dfa_final_states.append(x)
                            break

    context["response_nfa_pandas"] = result.objects.all().last()

    return render(request,"Home/index.html",context)

