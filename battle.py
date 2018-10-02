from locators.mainpages import Mainpages as mp
from locators.inbattle import Inbattle as ib
from algorithms import Algorithms as al
import configparser
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from random import *
import collections
from gamestate import GameState

class Battle():

    def __init__(self):
        config = configparser.ConfigParser()
        conf_file = 'config.ini' 
        config.read(conf_file)
        self.chromedriver = config['PATHS']['chromedriver']
        self.url = config['CREDENTIALS']['url']
        self.uid = config['CREDENTIALS']['uid']
        self.pwd = config['CREDENTIALS']['pwd']
        self.localpath = config['PATHS']['localpath']
        opponent_str = config['DEFAULT']['opponents']
        self.opponents = opponent_str.split(',')
        self.SHORT_WAIT = 1
        self.MEDIUM_WAIT = 5
        self.LONG_WAIT = 10
        self.UNRATED_WAIT = 180
        self.RATED_WAIT = 300
        self.battle_algorithm = config['ALGORITHMS']['battle']
        self.game_over = True
        #TODO: Make certain variables global such as verbosity
        self.verbosity_flag = True
        self.mega_flag = False
        self.zmove_flag = False
        self.game_state = GameState()
        self.driver = self.start_driver()
        
    def start_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--headless")
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL' , 'performance': 'ALL'}
        '''For this call:
        for entry in driver.get_log('browser'):
            print entry'''
        #s = ["--verbose", "--log-path=" + self.localpath + "\\session.log"]
        return webdriver.Chrome(self.chromedriver, options = chrome_options, desired_capabilities = d)#, service_args = s)

    def verbosity(self, print_statement):
        if self.verbosity_flag == True:
            print(print_statement)

    def login(self):
        driver = self.driver
        url = self.url
        uid = self.uid
        pwd = self.pwd
        driver.get(url)
        elem = WebDriverWait(driver, self.MEDIUM_WAIT).until(EC.presence_of_element_located((mp.user_btn_loc)))
        elem.click()
        driver.find_element(*mp.user_input_loc).send_keys(uid)
        driver.find_element(*mp.submit_btn_loc).click()
        elem = WebDriverWait(driver, self.MEDIUM_WAIT).until(EC.presence_of_element_located((mp.pwd_input_loc)))
        driver.find_element(*mp.pwd_input_loc).send_keys(pwd)
        driver.find_element(*mp.submit_btn_loc).click()

    def upload_team(self, team_path_ext):
        driver = self.driver
        team_path = team_path_ext.split('.')[0]
        if '\\' in team_path_ext:
            path_list = team_path.split('\\')
            team_name = path_list.pop()
        elif '/' in team_path_ext:
            path_list = team_path.split('/')
            team_name = path_list.pop()
        else: 
            team_name = team_path
        team_file = open(team_path_ext)
        #open teambuilder
        driver.find_element(*mp.teambuilder_btn_loc).click()
        #select format folder
        elem = WebDriverWait(driver, self.MEDIUM_WAIT).until(EC.presence_of_element_located((mp.addformatfolder_select_loc)))
        time.sleep(self.SHORT_WAIT)
        elem.click()
        time.sleep(self.SHORT_WAIT)
        driver.find_element(*mp.gen7ou_btn_loc).click()
        #new team
        driver.find_element(*mp.newteam_btn_loc).click()
        #import from text
        driver.find_element(*mp.import_btn_loc).click()
        #choose name
        driver.find_element(*mp.teamname_input_loc).click()
        driver.find_element(*mp.teamname_input_loc).send_keys('')
        driver.find_element(*mp.teamname_input_loc).send_keys(team_name)
        #enter team
        driver.find_element(*mp.teamedit_textbox_loc).send_keys(team_file.read())
        #save
        driver.find_element(*mp.save_btn_loc).click()

    def challenge_user(self, username):
        #TODO: The entire function
        #open find user
        #enter user name
        #confirm
        #select format and team
        #challenge
        pass

    def accept_challenge(self, user, challenge_elem):
        '''
        Pass in the correct locator so that only the right challenge is accepted. Format related information may need to be set as well in future rewrites.
        '''
        challenge_elem.find_element(*mp.acceptchallenge_btn_loc).click()

    def switch_active_tab(self, tab):
        '''
        Use this unless you don't care about staying logged in or have those credentials saved.
        '''
        locator = tab + "_tab_loc"
        self.driver.find_element(*getattr(mp, locator)).click()

    def poll_challenge(self, users):
        '''
        Loop and wait for a challenge to come in. Check it and accept if desired.
        '''
        while True:
            pms = self.driver.find_elements(*mp.pm_div_loc)
            for pm in pms:
                if len(pm.find_elements(*mp.challenge_div_loc)) > 0:
                    user = pm.find_element_by_tag_name("h3").text
                    if user in users:
                        self.accept_challenge(user, pm.find_element(*mp.challenge_div_loc))
                        return
            self.verbosity("Starting a 5 second wait before polling again...")
            time.sleep(self.MEDIUM_WAIT)


    def switch_active_tab_by_url(self, url):
        '''
        Try not to use this as it seems to log the user out for some reason.
        '''
        driver = self.driver
        if url.lower() == "home":
            driver.get(self.url)
        else:
            driver.get(self.url + '/' + url)
    
    def battle_loop(self, wait_time):
        '''
        Run a loop that constantly polls for battle updates until it terminates. 
        '''
        self.verbosity("Battle is starting!")
        self.game_state = GameState()
        #Have one clause for choosing a lead
        #Loop through the turns until the game ends
        self.game_over = False
        self.zoom_out()
        is_first_turn = True
        self.verbosity("-----------------------------------")
        while self.is_game_over() == False:
            self.verbosity("OUTPUTTING LOG AT START OF TURN")
            '''for entry in self.driver.get_log('browser'):
                print(entry)'''
            self.verbosity("TURN WILL NOW BEGIN")
            if is_first_turn == True:
                self.verbosity("Choosing starter.")
                self.choose_starter()
                self.verbosity("Starter chosen.")
                is_first_turn = False
            else:
                self.verbosity("Selecting a move.")
                self.select_action(wait_time)
            try:
                elem = WebDriverWait(driver, self.SHORT_WAIT).until(EC.presence_of_element_located((ib.starter_btn_loc)))
                elem.click()
            except:
                pass
            self.verbosity("-----------------------------------")
        self.verbosity("Battle has ended.")
    
    def zoom_out(self):
        '''
        Zoom the screen out so that the UI is more consistent. Think of this as an extra maximize window.
        '''
        driver = self.driver
        try:
            elem = driver.find_element(*ib.selectswitch_btn_loc)
            driver.execute_script("document.body.style.zoom='90%';")
        except:
            self.verbosity("Proceeding with run execution. No more resizing.")
    
    def choose_starter(self):
        driver = self.driver
        game_state = collections.OrderedDict()
        elem = WebDriverWait(driver, self.UNRATED_WAIT).until(EC.presence_of_element_located((ib.starter_btn_loc)))
        game_state['starter'] = driver.find_elements(*ib.starter_btn_loc)
        chosen_starter = getattr(al, self.battle_algorithm)(driver, game_state)
        elem = self.parse_move_dict(game_state, chosen_starter)
        elem.click()

    def select_action(self, wait_time):
        #Poll until selectable options are available
        #Determine best action going by weights of existing options (or just make it random)
        driver = self.driver
        elem = WebDriverWait(driver,wait_time).until(lambda driver: driver.find_elements(*ib.move_btn_loc) or driver.find_elements(*ib.switch_btn_loc))
        #self.verbosity("These are the current move options: ")
        if len(elem) == 0:
            return True
        self.verbosity("Options are available.")
        #provide the current game state for the algorithm... should this be saved somewhere instead of constantly passed?
        #logic: moves should be enabled if zmove enabled is false, switches should be enabled if zmove enabled is false
        move_dict = collections.OrderedDict()
        '''if len(driver.find_elements(*ib.zmove_btn_loc)) > 0 and self.zmove_flag == False:
            game_state['zmove'] = len(driver.find_elements(*ib.zmove_btn_loc))
        elif len(driver.find_elements(*ib.movezenabled_btn_loc)) > 0:
            game_state['movezenabled'] = len(driver.find_elements(*ib.movezenabled_btn_loc))
        if len(driver.find_elements(*ib.move_btn_loc)) > 0 and self.zmove_flag == False:
            game_state['move'] = len(driver.find_elements(*ib.move_btn_loc))
        if len(driver.find_elements(*ib.switch_btn_loc)) > 0:
            if self.mega_flag == True:
                self.mega_flag = False
            elif self.zmove_flag == True:
                self.zmove_flag = False
            else:
                game_state['switch'] = len(driver.find_elements(*ib.switch_btn_loc))
        if len(driver.find_elements(*ib.megaevo_btn_loc)) > 0:
            game_state['megaevo'] = len(driver.find_elements(*ib.megaevo_btn_loc))'''
        #TODO: Implement logic to use Z-moves and mega evolution at the appropriate times.
        if len(driver.find_elements(*ib.move_btn_loc)) > 0:
            try:
                elem = WebDriverWait(driver, self.SHORT_WAIT).until(EC.presence_of_element_located((ib.zmove_btn_loc)))
                #zmove_elem = find_element(*ib.zmove_btn_loc)
                move_dict['move'] = driver.find_element(*ib.movenoz_div_loc).find_elements(*ib.move_btn_loc)
            except:
                move_dict['move'] = driver.find_element(*ib.move_div_loc).find_elements(*ib.move_btn_loc)
        if len(driver.find_elements(*ib.switch_btn_loc)) > 0:
            move_dict['switch'] = driver.find_elements(*ib.switch_btn_loc)
        
        chosen_move = getattr(al, self.battle_algorithm)(self.driver, move_dict)
        elem = self.parse_move_dict(move_dict, chosen_move)
        elem.click()

    def parse_move_dict(self, game_state, move_index):
        #driver = self.driver
        self.verbosity("The next move will be: [" + str(move_index) + "]")
        searched_index = move_index
        #Example if somehow all moves were available
        #0,1,2,3,4,5,6,7,8,9,10
        #move: 0,1,2,3 len = 4 
        #switch:4,5,6,7,8 len = 5
        #mega:9 len = 1
        #z: 10 len = 1
        range_statement = "The possible options for this turn are:"
        adjusted_index = 0
        for key, elem in game_state.items():
            value = len(elem)
            start_index = adjusted_index + 1
            adjusted_index = adjusted_index + value
            range_statement = range_statement + "\nmove type: [" + key + "] between the range: [" + str(start_index) + "] and [" + str(adjusted_index) + "]"
        self.verbosity(range_statement)
        for key, elem in game_state.items():
            value = len(elem)
            if searched_index <= value:
                self.verbosity("Move type will be: " + key)
                self.verbosity("Move index will be: " + str(searched_index-1))
                locator = elem#getattr(ib, key + "_btn_loc")
                #TODO: Fix these key calls once implemented. FSM is probably the best option here.
                if key == "megaevo": 
                    self.mega_flag = not self.mega_flag
                if key == "zmove":
                    self.zmove_flag = not self.zmove_flag
                return locator[searched_index-1]#driver.find_elements(*locator)[searched_index-1]
            searched_index = searched_index - value
        #TODO: Add an error check here
        return None
    
    def is_game_over(self):
        return self.game_over

    def run(self):
        team_file = "data\\dps.txt" #This should be gotten from the config file or at least dynamically generated.
        opponents = self.opponents
        self.login()
        self.upload_team(team_file)
        self.switch_active_tab("home")
        self.poll_challenge(opponents)
        self.battle_loop(self.RATED_WAIT)
    

if __name__ == "__main__":
    battleobj = Battle()
    battleobj.run()