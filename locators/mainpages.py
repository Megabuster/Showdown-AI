from selenium.webdriver.common.by import By

class Mainpages():
    #left side
    format_drop_loc = (By.CSS_SELECTOR, ".formatselect")
    team_drop_loc = (By.CSS_SELECTOR, ".teamselect")
    battle_btn_loc = (By.CSS_SELECTOR, "button[name='search']")
    teambuilder_btn_loc = (By.CSS_SELECTOR, "button[value='teambuilder']")
    ladder_btn_loc = (By.CSS_SELECTOR, "button[value='ladder']")
    watch_btn_loc = (By.CSS_SELECTOR, "button[name='battles']")
    find_btn_loc = (By.CSS_SELECTOR, "button[name='finduser']")
    #right side
    user_btn_loc = (By.NAME, "login")
    user_input_loc = (By.CSS_SELECTOR, ".textbox")
    hide_btn_loc = (By.NAME, "closeHide")
    #user pop up
    submit_btn_loc = (By.CSS_SELECTOR, "button[type='submit']")
    close_btn_loc = (By.NAME, "close")
    pwd_input_loc = (By.NAME, "password")
    #format select (add more if needed)
    format_popup_loc = (By.CSS_SELECTOR, ".ps-popup")
    gen7rand_btn_loc = (By.CSS_SELECTOR, "button[value='gen7randombattle']")
    gen7unrated_btn_loc = (By.CSS_SELECTOR, "button[value='gen7unratedrandombattle']")
    gen7ou_btn_loc = (By.CSS_SELECTOR, "button[value='gen7ou']")
    gen7ubers_btn_loc = (By.CSS_SELECTOR, "button[value='gen7ubers']")
    #team builder
    newteam_btn_loc = (By.CSS_SELECTOR, "button[name='newTop']")
    addformatfolder_select_loc = (By.CSS_SELECTOR, "div[class='selectFolder'][data-value='+']")
    addfolder_select_loc = (By.CSS_SELECTOR, "div[class='selectFolder][data-value='++']")
    #team edit
    teamname_input_loc = (By.CSS_SELECTOR, ".teamnameedit")
    import_btn_loc = (By.CSS_SELECTOR, "button[name='import']")
    addpokemon_btn_loc = (By.CSS_SELECTOR, "button[name='addPokemon']")
    teamedit_textbox_loc = (By.CSS_SELECTOR, ".teamedit > .textbox")
    save_btn_loc = (By.CSS_SELECTOR, ".savebutton")
    back_btn_loc = (By.CSS_SELECTOR, "button[name='back']")
    validate_btn_loc = (By.CSS_SELECTOR, "button[name='validate']")
    #tabs
    home_tab_loc = (By.CSS_SELECTOR, ".fa-home")
    teambuilder_tab_loc = (By.CSS_SELECTOR, ".fa-pencil-square-o")
    room_tab_loc = (By.CSS_SELECTOR, ".roomtab")
    #user prompt
    challenge_btn_loc = (By.NAME, "challenge")
    chat_btn_loc = (By.NAME, "pm")
    useroptions_btn_loc = (By.NAME, "userOptions")
    #challenge box (once a user has been selected)
    makechallenge_btn_loc = (By.NAME, "makeChallenge")
    dismisschallenge_btn_loc = (By.NAME, "dismissChallenge")
    challenge_div_loc = (By.CSS_SELECTOR, ".challenge")
    acceptchallenge_btn_loc = (By.NAME, "acceptChallenge")
    rejectchallenge_btn_loc = (By.NAME, "rejectChallenge")
    #multiple things can have a pm window, so nest this as needed
    pm_div_loc = (By.CSS_SELECTOR, ".pm-window")