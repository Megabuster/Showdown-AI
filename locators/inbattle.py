from selenium.webdriver.common.by import By

class Inbattle():

    #timer
    timer_btn_loc = (By.NAME, "openTimer")
    #choose lead (this gives the entire list of them and needs to be indexed further)
    starter_btn_loc = (By.NAME, "chooseTeamPreview")
    #take the list and do elem[index].text for each one to link the names
    move_div_loc = (By.CSS_SELECTOR,".movemenu")
    movenoz_div_loc = (By.CSS_SELECTOR, ".movebuttons-noz")
    move_btn_loc = (By.CSS_SELECTOR, "button[name='chooseMove']")
    movez_div_loc = (By.CSS_SELECTOR, ".movebuttons-z")
    switch_btn_loc = (By.CSS_SELECTOR, "button[name='chooseSwitch']")
    megaevo_btn_loc = (By.NAME, "megaevo")
    zmove_btn_loc = (By.NAME, "zmove")
    starter_btn_loc = (By.NAME, "chooseTeamPreview")
    #battle pace controls
    selectmove_btn_loc = (By.NAME, "selectMove")
    selectswitch_btn_loc = (By.NAME, "selectSwitch")
    gotoend_btn_loc = (By.NAME, "goToEnd")