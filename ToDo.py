import customtkinter as ctk 

class ToDoList(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("To-Do List:")

        self.geometry("500x600")


        ctk.set_appearance_mode("system")

        ctk.set_default_color_theme("blue")


        self.title_label = ctk.CTkLabel(self,
                                        text = "My To do list:", 
                                        font = ctk.CTkFont(size = 20, 
                                                           weight = "bold"))

        self.title_label.pack(pady=20)

        
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady = 10, padx= 10, fill = "x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text= "Enter new task.", width= 300)
        self.task_entry.pack(side = "left", padx = (0, 5), fill = "x", expand = True)
        self.task_entry.bind("<Return>",
                             self.add_task_event_enter_key)
        
        self.add_botton = ctk.CTkButton(self.input_frame,
                                        text = "Add",
                                        width = 80,
                                        command= self.add_task_event)
        self.add_botton.pack(side = "left")

        self.tasks_list_frame = ctk.CTkScrollableFrame(self, height = 400)
        self.tasks_list_frame.pack(pady = 10, padx = 10, fill = "both", expand = True)

        self.tasks = []

    def add_task_event_enter_key(self, event):
        self.add_task_event()
    

    def add_task_event(self):
        task_text = self.task_entry.get()

        if task_text:
            self.creat_new_task_ui(task_text)

            self.task_entry.delete(0,"end")

        else:
            print("Task cannot be empty.")

    
    def creat_new_task_ui(self, task_text):
        task_item_frame = ctk.CTkFrame(self.tasks_list_frame, fg_color = ("gray90","gray25"))
        task_item_frame.pack(fill= "x", pady = 5, padx= 5)

        checkbox_var = ctk.StringVar(value = "off")

        task_checkbox = ctk.CTkCheckBox(task_item_frame, text = "",
                                        variable = checkbox_var,
                                        onvalue = "on",
                                        offvalue="off",
                                        width= 20)
        task_checkbox.pack(side = "left",
                           padx = 5)
        
        task_lable = ctk.CTkLabel(task_item_frame, 
                                  text = task_text,
                                  wraplength = 280,
                                  justify = "left")
        
        task_lable.pack(side = "left",
                        fill = "x",
                        expand = True,
                        padx = 5)
        
        edit_button = ctk.CTkButton(task_item_frame, 
                                    text = "Edit",
                                    width= 60,)
        edit_button.pack(side = "left",
                         padx = (0,5))
        
        delete_button = ctk.CTkButton(task_item_frame,
                                     text= "Delete",
                                     width= 60,
                                     fg_color= "tomato")
        delete_button.pack(side = "left")

        task_data = {
            "text": task_text,
            "completed" : False,
            "checkbox_var": checkbox_var,
            "checkbox_widget":task_checkbox,
            "label_widget": task_lable,
            "edit_button": edit_button,
            "delete_button": delete_button,
            "frame_widget": task_item_frame,
            "is_editing": False,
            "edit_entry_widget": None
        }

        self.tasks.append(task_data)


        task_checkbox.configure(command = lambda current_task_data = task_data:
                                self.toggle_task_complete(current_task_data))
        delete_button.configure(command = lambda current_task_data = task_data: 
                                self.delete_task(current_task_data))
        edit_button.configure(command = lambda current_task_data = task_data:
                                self.handle_edit_save_task(current_task_data))


    def toggle_task_complete(self, task_data):
        task_data["completed"] = not task_data["completed"]

        font_to_use = ctk.CTkFont(size= 12)

        default_text_color = task_data["label_widget"].cget("text_color")

        if task_data["completed"]:
            font_to_use = ctk.CTkFont(size= 12,
                                      slant= "italic",
                                      overstrike= True)
            task_data["label_widget"].configure(text_color = "gray")
        else:
            task_data["label_widget"].configure(font = font_to_use)

        if task_data["completed"]:
            task_data["checkbox_var"].set("on")
        else:
            task_data["checkbox_var"].set("off")


    def delete_task(self, task_data_to_delete):
        task_data_to_delete["frame_widget"].destroy()

        if task_data_to_delete in self.tasks:
            self.tasks.remove(task_data_to_delete)


    def handle_edit_save_task(self, task_data):
        if not task_data["is_editing"]:
            task_data["is_editing"] = True
            task_data["label_widget"].pack_forget()

            edit_entry = ctk.CTkEntry(task_data["frame_widget"])
            edit_entry.insert(0, task_data["text"])
            edit_entry.pack(side = "left",
                        fill = "x",
                        expand = True,
                        padx = 5,
                        after = task_data["checkbox_widget"],
                        before = task_data["edit_button"])
            
            edit_entry.focus_set()

            edit_entry.bind("<Return>",
                            lambda event, td = task_data:
                            self.handle_edit_save_task(td))
            
            task_data["edit_entry_widget"] = edit_entry

            task_data["edit_button"].configure(text = "Save",
                                               fg_color = "green")
        else:
            if task_data["edit_entry_widget"]:
                new_text = task_data["edit_entry_widget"].get()
                if new_text.strip():
                    task_data["text"] = new_text
                    task_data["label_widget"].configure(text = new_text)

                task_data["edit_entry_widget"].destroy()
                task_data["edit_entry_widget"] = None

            task_data["label_widget"].pack(side = "left",
                                           fill = "x",
                                           expand = True,
                                           padx = 5,
                                           after = task_data["checkbox_widget"],
                                           before = task_data["edit_button"])
            
            task_data["edit_button"].configure(text = "Edit",
                                               fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            task_data["is_editing"] = False

if __name__ == "__main__":
    app = ToDoList()

    app.mainloop()