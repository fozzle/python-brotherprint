import re
'''Brother Python EscP Command Library

Description:
A collection of functions to more easily facilitate printing to the Brother QL label
printers without having to memorize the ESC/P commands. Also handles sending to sockets
for you.
'''


class BrotherPrint:
    
    font_types = {'bitmap': 0,
                  'outline': 1}
    
    def __init__(self, fsocket):
        self.fsocket = fsocket
        self.fonttype = self.font_types['bitmap']
    
    ###########################################################################
    # System Commands & Settings
    ###########################################################################
    
    def raster_mode(self):
        '''Sets printer to raster mode
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        '''
        self.send(chr(27)+'ia'+chr(1))
    
    def template_mode(self):
        '''Sets printer to template mode
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(27)+'i'+'a'+'3')
    
    def command_mode(self):
        '''Calling this function sets the printer to ESC/P command mode.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(27)+chr(105)+chr(97)+'0')
    
    def initialize(self):
        '''Calling this function initializes the printer.
    
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.fonttype = self.font_types['bitmap']
        self.send(chr(27)+chr(64))
        
    def select_charset(self, charset):
        '''Select international character set and changes codes in code table accordingly
        
        Args:
            charset: String. The character set we want.
        Returns:
            None
        Raises:
            RuntimeError: Invalid charset.
        '''
        charsets = {'USA':0,
                   'France':1,
                   'Germany':2,
                   'UK':3, 
                   'Denmark':4,
                   'Sweden':5, 
                   'Italy':6, 
                   'Spain':7,
                   'Japan':8, 
                   'Norway':9, 
                   'Denmark II':10, 
                   'Spain II':11, 
                   'Latin America':12, 
                   'South Korea':13, 
                   'Legal':64, 
                   }
        if charset in charsets:
            self.send(chr(27)+'R'+chr(charsets[charset]))
        else:
            raise RuntimeError('Invalid charset.')
    
    def select_char_code_table(self, table):
        '''Select character code table, from tree built in ones.
        
        Args:
            table: The desired character code table. Choose from 'standard', 'eastern european', 'western european', and 'spare'
        Returns:
            None
        Raises:
            RuntimeError: Invalid chartable.
        '''
        tables = {'standard': 0,
                  'eastern european': 1,
                  'western european': 2,
                  'spare': 3
                  }
        if table in tables:
            self.send(chr(27)+'t'+chr(tables[table]))
        else:
            raise RuntimeError('Invalid char table.')
    
    def cut_setting(self, cut):
        '''Set cut setting for printer. 
        
        Args:
            cut: The type of cut setting we want. Choices are 'full', 'half', 'chain', and 'special'.
        Returns:
            None
        Raises:
            RuntimeError: Invalid cut type.
        '''
        
        cut_settings = {'full' : 0b00000001,
                        'half' : 0b00000010,
                        'chain': 0b00000100,
                        'special': 0b00001000
                        }
        if cut in cut_settings:
            self.send(chr(27)+'iC'+chr(cut_settings[cut]))
        else:
            raise RuntimeError('Invalid cut type.')
        
        
    ###########################################################################
    # Format Commands
    ###########################################################################
    def rotated_printing(self, action):
        '''Calling this function applies the desired action to the printing orientation
        of the printer.
        
        Args:
            action: The desired printing orientation. 'rotate' enables rotated printing. 'normal' disables rotated printing.
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action=='rotate':
            action='1'
        elif action=='cancel':
            action='0'
        else:
            raise RuntimeError('Invalid action.')
        self.send(chr(27)+chr(105)+chr(76)+action)
    
    def feed_amount(self, amount):
        '''Calling this function sets the form feed amount to the specified setting.
    
        Args:
            amount: the form feed setting you desire. Options are '1/8', '1/6', 'x/180', and 'x/60',
            with x being your own desired amount. X must be a minimum of 24 for 'x/180' and 8 for 'x/60'
        Returns:
            None
        Raises:
            None
        '''
        n = None
        if amount=='1/8':
            amount = '0'
        elif amount=='1/6':
            amount = '2'
        elif re.search('/180', amount):
            n = re.search(r"(\d+)/180", amount)
            n = n.group(1)
            amount = '3'
        elif re.search('/60', amount):
            n = re.search(r"(\d+)/60", amount)
            n = n.group(1)
            amount = 'A'
        if n:
            self.send(chr(27)+amount+n)
        else:
            self.send(chr(27)+amount)
    
    def page_length(self, length):
        '''Specifies page length. This command is only valid with continuous length labels.
        
        Args:
            length: The length of the page, in dots. Can't exceed 12000.
        Returns:
            None
        Raises:
            RuntimeError: Length must be less than 12000.
        '''
        mH = length/256
        mL = length%256
        if length < 12000:
            self.send(chr(27)+'('+'C'+chr(2)+chr(0)+chr(mL)+chr(mH))
        else:
            raise RuntimeError('Length must be less than 12000.')
        
    def page_format(self, topmargin, bottommargin):
        '''Specify settings for top and bottom margins. Physically printable area depends on media.
        
        Args:
            topmargin: the top margin, in dots. The top margin must be less than the bottom margin.
            bottommargin: the bottom margin, in dots. The bottom margin must be less than the top margin.
        Returns:
            None
        Raises:
            RuntimeError: Top margin must be less than the bottom margin.
        '''
        tL = topmargin%256
        tH = topmargin/256
        BL = bottommargin%256
        BH = topmargin/256
        if (tL+tH*256) < (BL + BH*256):
            self.send(chr(27)+'('+'c'+chr(4)+chr(0)+chr(tL)+chr(tH)+chr(BL)+chr(BH))
        else:
            raise RuntimeError('The top margin must be less than the bottom margin')
        
    def left_margin(self, margin):
        '''Specify the left margin.
        
        Args:
            margin: The left margin, in character width. Must be less than the media's width.
        Returns:
            None
        Raises:
            RuntimeError: Invalid margin parameter.
        '''
        if margin <= 255 and margin >= 0:
            self.send(chr(27)+'I'+chr(margin))
        else:
            raise RuntimeError('Invalid margin parameter.')
    
    def right_margin(self, margin):
        '''Specify the right margin.
        
        Args:
            margin: The right margin, in character width, must be less than the media's width.
        Returns:
            None
        Raises:
            RuntimeError: Invalid margin parameter
        '''
        if margin >=1 and margin <=255:
            self.send(chr(27)+'Q'+chr(margin))
        else:
            raise RuntimeError('Invalid margin parameter in function rightMargin')
    
    def horz_tab_pos(self, positions):
        '''Sets tab positions, up to a maximum of 32 positions. Also can clear tab positions.
        
        Args:
            positions: either a list of tab positions (between 1 and 255), or 'clear'.
        Returns:
            None
        Raises:
            RuntimeError: Invalid position parameter.
            RuntimeError: Too many positions.
        '''
        if positions == 'clear':
            self.send(chr(27)+'D'+chr(0))
            return
        if positions.min < 1 or positions.max >255:
                raise RuntimeError('Invalid position parameter in function horzTabPos')
        sendstr = chr(27) + 'D'
        if len(positions)<32:
            for position in positions:
                sendstr += chr(position)
            self.send(sendstr+chr(0))
        else:
            raise RuntimeError('Too many positions in function horzTabPos')
        
    def vert_tab_pos(self, positions):
        '''Sets tab positions, up to a maximum of 32 positions. Also can clear tab positions.
        
        Args:
            positions -- Either a list of tab positions (between 1 and 255), or 'clear'.
        Returns:
            None
        Raises:
            RuntimeError: Invalid position parameter.
            RuntimeError: Too many positions.
        '''
        if positions == 'clear':
            self.send(chr(27)+'B'+chr(0))
            return
        if positions.min < 1 or positions.max >255:
                raise RuntimeError('Invalid position parameter in function horzTabPos')
        sendstr = chr(27) + 'D'
        if len(positions)<=16:
            for position in positions:
                sendstr += chr(position)
            self.send(sendstr + chr(0))
        else:
            raise RuntimeError('Too many positions in function vertTabPos')
    
    
    ############################################################################
    # Print Operations
    ############################################################################
    def send(self, text):
        '''Sends text to printer
        
        Args:
            text: string to be printed
        Returns:
            None
        Raises:
            None'''
        self.fsocket.send(text)
        
    def forward_feed(self, amount):
        '''Calling this function finishes input of the current line, then moves the vertical 
        print position forward by x/300 inch.
        
        Args:
            amount: how far foward you want the position moved. Actual movement is calculated as 
            amount/300 inches.
        Returns:
            None
        Raises:
            RuntimeError: Invalid foward feed.
        '''
        if amount <= 255 and amount >=0:
            self.send(chr(27)+'J'+chr(amount))
        else:
            raise RuntimeError('Invalid foward feed, must be less than 255 and >= 0')
    
    def abs_vert_pos(self, amount):
        '''Specify vertical print position from the top margin position.
        
        Args:
            amount: The distance from the top margin you'd like, from 0 to 32767
        Returns:
            None
        Raises:
            RuntimeError: Invalid vertical position.
        '''
        mL = amount%256
        mH = amount/256
        if amount < 32767 and amount > 0:
            self.send(chr(27)+'('+'V'+chr(2)+chr(0)+chr(mL)+chr(mH))
        else:
            raise RuntimeError('Invalid vertical position in function absVertPos')
        
    def abs_horz_pos(self, amount):
        '''Calling this function sets the absoulte print position for the next data, this is
        the position from the left margin.
        
        Args:
            amount: desired positioning. Can be a number from 0 to 2362. The actual positioning
            is calculated as (amount/60)inches from the left margin.
        Returns:
            None
        Raises:
            None
        '''
        n1 = amount%256
        n2 = amount/256
        self.send(chr(27)+'${n1}{n2}'.format(n1=chr(n1), n2=chr(n2)))
    
    def rel_horz_pos(self, amount):
        '''Calling this function sets the relative horizontal position for the next data, this is
        the position from the current position. The next character will be printed (x/180)inches
        away from the current position. The relative position CANNOT be specified to the left.
        This command is only valid with left alignment.
        
        Args:
            amount: desired positioning. Can be a number from 0 to 7086. The actual positioning
            is calculated as (amount/180)inches from the current position.
        Returns:
            None
        Raises:
            None
        '''
        n1 = amount%256
        n2 = amount/256
        self.send(chr(27)+'\{n1}{n2}'.format(n1=chr(n1),n2=chr(n2)))

    def alignment(self, align):
        '''Sets the alignment of the printer.
        
        Args:
            align: desired alignment. Options are 'left', 'center', 'right', and 'justified'. Anything else
            will throw an error.
        Returns:
            None
        Raises:
            RuntimeError: Invalid alignment.
        '''
        if align=='left':
            align = '0'
        elif align=='center':
            align = '1'
        elif align=='right':
            align = '2'
        elif align=='justified':
            align = '3'
        else:
            raise RuntimeError('Invalid alignment in function alignment')
        self.send(chr(27)+'a'+align)
    
    def carriage_return(self):
        '''Performs a line feed amount, sets next print position to the beginning of the next line,
        will ignore a subsequent line feed command.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(13))
    
    def line_feed(self):
        '''Performs line feed operation, any carriage return command subsequent to a lineFeed will
        be ignored.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(10))
        
    def page_feed(self):
        '''Page feed.
        
        Keyword arguments:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(12))
        
    def print_page(self, cut):
        '''End input, set cut setting, and pagefeed.
        
        Args:
            cut: cut setting, choose from 'full', 'half', 'special' and 'chain'
        Returns:
            None
        Raises:
            None
        '''
        self.cut_setting(cut)
        self.page_feed()
        
    def frame(self, action):
        '''Places/removes frame around text
        
        Args:
            action -- Enable or disable frame. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        choices = {'on': '1',
                   'off': '0'}
        if action in choices:
            self.send(chr(27)+'if'+choices[action])
        else:
            raise RuntimeError('Invalid action for function frame, choices are on and off')
        
    def horz_tab(self):
        '''Applies horizontal tab to nearest tab position
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(9))
        
    def vert_tab(self):
        '''Applies vertical tab to nearest vertical tab position
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(11))
    ###########################################################################
    # Text Operations
    ###########################################################################
    def bold(self, action):
        '''Enable/cancel bold printing
        
        Args:
            action: Enable or disable bold printing. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action =='on':
            action = 'E'
        elif action == 'off':
            action = 'F'
        else:
            raise RuntimeError('Invalid action for function bold. Options are on and off')
        self.send(chr(27)+action)
        
    def italic(self, action):
        '''Enable/cancel italic printing
        
        Args:
            action: Enable or disable italic printing. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action =='on':
            action = '4'
        elif action=='off':
            action = '5'
        else:
            raise RuntimeError('Invalid action for function italic. Options are on and off')
        self.send(chr(27)+action)
        
    def double_strike(self, action):
        '''Enable/cancel doublestrike printing
        
        Args:
            action: Enable or disable doublestrike printing. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action == 'on':
            action = 'G'
        elif action == 'off':
            action = 'H'
        else:
            raise RuntimeError('Invalid action for function doubleStrike. Options are on and off')
        self.send(chr(27)+action)
        
    def double_width(self, action):
        '''Enable/cancel doublewidth printing
        
        Args:
            action: Enable or disable doublewidth printing. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action == 'on':
            action = '1'
        elif action == 'off':
            action = '0'
        else:
            raise RuntimeError('Invalid action for function doubleWidth. Options are on and off')
        self.send(chr(27)+'W'+action)
        
    def compressed_char(self, action):
        '''Enable/cancel compressed character printing
        
        Args:
            action: Enable or disable compressed character printing. Options are 'on' and 'off'
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        if action == 'on':
            action = 15
        elif action == 'off':
            action = 18
        else:
            raise RuntimeError('Invalid action for function compressedChar. Options are on and off')
        self.send(chr(action))
        
    def underline(self, action):
        '''Enable/cancel underline printing
        
        Args:
            action -- Enable or disable underline printing. Options are '1' - '4' and 'cancel'
        Returns:
            None
        Raises:
            None
        '''
        if action == 'off':
            action = '0'
            self.send(chr(27)+chr(45)+action)
        else:
            self.send(chr(27)+chr(45)+action)
        
    def char_size(self, size):
        '''Changes font size
        
        Args:
            size: change font size. Options are 24' '32' '48' for bitmap fonts 
            33, 38, 42, 46, 50, 58, 67, 75, 83, 92, 100, 117, 133, 150, 167, 200 233, 
            11, 44, 77, 111, 144 for outline fonts.
        Returns:
            None
        Raises:
            RuntimeError: Invalid font size.
            Warning: Your font is currently set to outline and you have selected a bitmap only font size
            Warning: Your font is currently set to bitmap and you have selected an outline only font size
        '''
        sizes = {'24':0,
                   '32':0,
                   '48':0,
                   '33':0, 
                   '38':0,
                   '42':0, 
                   '46':0, 
                   '50':0,
                   '58':0, 
                   '67':0, 
                   '75':0, 
                   '83':0, 
                   '92':0, 
                   '100':0, 
                   '117':0, 
                   '133':0, 
                   '150':0, 
                   '167':0, 
                   '200':0, 
                   '233':0, 
                   '11':1, 
                   '44':1, 
                   '77':1, 
                   '111':1, 
                   '144':1
                   }
        if size in sizes:
            if size in ['24','32','48'] and self.fonttype != self.font_types['bitmap']:
                raise Warning('Your font is currently set to outline and you have selected a bitmap only font size')
            if size not in ['24', '32', '48'] and self.fonttype != self.font_types['outline']:
                raise Warning('Your font is currently set to bitmap and you have selected an outline only font size')
            self.send(chr(27)+'X'+chr(0)+chr(int(size))+chr(sizes[size]))
        else:
            raise RuntimeError('Invalid size for function charSize, choices are auto 4pt 6pt 9pt 12pt 18pt and 24pt')
        
    def select_font(self, font):
        '''Select font type
        
        Choices are: 
        <Bit map fonts>
        'brougham'
        'lettergothicbold'
        'brusselsbit'
        'helsinkibit'
        'sandiego'
        <Outline fonts>
        'lettergothic'
        'brusselsoutline'
        'helsinkioutline'
        
        Args:
            font: font type
        Returns:
            None
        Raises:
            RuntimeError: Invalid font.
        '''
        fonts = {'brougham': 0, 
                 'lettergothicbold': 1, 
                 'brusselsbit' : 2, 
                 'helsinkibit': 3, 
                 'sandiego': 4, 
                 'lettergothic': 9,
                 'brusselsoutline': 10, 
                 'helsinkioutline': 11}
        
        if font in fonts:
            if font in ['broughham', 'lettergothicbold', 'brusselsbit', 'helsinkibit', 'sandiego']:
                self.fonttype = self.font_types['bitmap']
            else:
                self.fonttype = self.font_types['outline']
                
            self.send(chr(27)+'k'+chr(fonts[font]))
        else:
            raise RuntimeError('Invalid font in function selectFont')
        
    def char_style(self, style):
        '''Sets the character style.
        
        Args:
            style: The desired character style. Choose from 'normal', 'outline', 'shadow', and 'outlineshadow'
        Returns:
            None
        Raises:
            RuntimeError: Invalid character style
        '''
        styleset = {'normal': 0,
                    'outline': 1,
                    'shadow': 2,
                    'outlineshadow': 3
                    }
        if style in styleset:
            self.send(chr(27) + 'q' + chr(styleset[style]))
        else:
            raise RuntimeError('Invalid character style in function charStyle')
    
    def pica_pitch(self):
        '''Print subsequent data with pica pitch (10 char/inch)
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(27)+'P')
        
    def elite_pitch(self):
        '''Print subsequent data with elite pitch (12 char/inch)
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(27)+'M')
    
    def micron_pitch(self):
        '''Print subsequent data with micron pitch (15 char/inch)
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(27)+'g')
    
    def proportional_char(self, action):
        '''Specifies proportional characters. When turned on, the character spacing set
        with charSpacing.
        
        Args:
            action: Turn proportional characters on or off.
        Returns:
            None
        Raises:
            RuntimeError: Invalid action.
        '''
        actions = {'off': 0,
                   'on': 1
                   }
        if action in actions:
            self.send(chr(27)+'p'+action)
        else:
            raise RuntimeError('Invalid action in function proportionalChar')
        
    def char_spacing(self, dots):
        '''Specifes character spacing in dots.
        
        Args:
            dots: the character spacing you desire, in dots
        Returns:
            None
        Raises:
            RuntimeError: Invalid dot amount.
        '''
        if dots in range(0,127):
            self.send(chr(27)+chr(32)+chr(dots))
        else:
            raise RuntimeError('Invalid dot amount in function charSpacing')
    
    ############################################################################
    # Bit Image
    ############################################################################
    
    # TODO: Complete bit image methods
    
        
        
        
    ############################################################################
    # Barcode 
    ############################################################################
    
    def barcode(self, data, format, characters='off', height=48, width='small', parentheses='on', ratio='3:1', equalize='off', rss_symbol='rss14std', horiz_char_rss=2):
        '''Print a standard barcode in the specified format
        
        Args:
            data: the barcode data
            format: the barcode type you want. Choose between code39, itf, ean8/upca, upce, codabar, code128, gs1-128, rss
            characters: Whether you want characters below the bar code. 'off' or 'on'
            height: Height, in dots.
            width: width of barcode. Choose 'xsmall' 'small' 'medium' 'large'
            parentheses: Parentheses deletion on or off. 'on' or 'off' Only matters with GS1-128
            ratio: ratio between thick and thin bars. Choose '3:1', '2.5:1', and '2:1'
            equalize: equalize bar lengths, choose 'off' or 'on'
            rss_symbol: rss symbols model, choose from 'rss14std', 'rss14trun', 'rss14stacked', 'rss14stackedomni', 'rsslimited', 'rssexpandedstd', 'rssexpandedstacked'
            horiz_char_rss: for rss expanded stacked, specify the number of horizontal characters, must be an even number b/w 2 and 20.
        '''
        
        barcodes = {'code39': '0',
                    'itf': '1',
                    'ean8/upca': '5',
                    'upce': '6',
                    'codabar': '9',
                    'code128': 'a',
                    'gs1-128': 'b',
                    'rss': 'c'}
        
        widths = {'xsmall': '0',
                  'small': '1',
                  'medium': '2',
                  'large': '3'}
        
        ratios = {'3:1': '0',
                  '2.5:1': '1',
                  '2:1': '2'}
        
        rss_symbols = {'rss14std': '0',
                       'rss14trun': '1',
                       'rss14stacked': '2',
                       'rss14stackedomni' : '3',
                       'rsslimited': '4',
                       'rssexpandedstd': '5',
                       'rssexpandedstacked': '6'
                       }
        
        character_choices = {'off': '0',
                      'on' : '1'}
        parentheses_choices = {'off':'1',
                               'on': '0'}
        equalize_choices = {'off': '0',
                            'on': '1'}
        
        sendstr = ''
        n2 = height/256
        n1 = height%256
        if format in barcodes and width in widths and ratio in ratios and characters in character_choices and rss_symbol in rss_symbols:
            sendstr += (chr(27)+'i'+'t'+barcodes[format]+'s'+'p'+'r'+character_choices[characters]+'u'+'x'+'y'+'h' + chr(n1) + chr(n2) +
                        'w'+widths[width]+'e'+parentheses_choices[parentheses]+'o'+rss_symbols[rss_symbol]+'c'+chr(horiz_char_rss)+'z'+ratios[ratio]+'f'+equalize_choices[equalize]
                        + 'b' + data + chr(92))
            if format in ['code128', 'gs1-128']:
                sendstr += chr(92)+ chr(92)
            self.send(sendstr)
        else:
            raise RuntimeError('Invalid parameters')
        
    ############################################################################
    # Template Commands
    ############################################################################
    
    def template_print(self):
        '''Print the page
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send('^FF')
    
    def choose_template(self, template):
        '''Choose a template
        
        Args:
            template: String, choose which template you would like.
        Returns:
            None
        Raises:
            None
        '''
        n1 = int(template)/10
        n2 = int(template)%10
        self.send('^TS'+'0'+str(n1)+str(n2))
        
    def machine_op(self, operation):
        '''Perform machine operations
        
        Args:
            operations: which operation you would like
        Returns:
            None
        Raises:
            RuntimeError: Invalid operation
        '''
        operations = {'feed2start': 1,
                      'feedone': 2,
                      'cut': 3
                      }
        
        if operation in operations:
            self.send('^'+'O'+'P'+chr(operations[operation]))
        else:
            raise RuntimeError('Invalid operation.')
            
    def template_init(self):
        '''Initialize command for template mode
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        self.send(chr(94)+chr(73)+chr(73))
        
    def print_start_trigger(self, type):
        '''Set print start trigger.
        
        Args:
            type: The type of trigger you desire.
        Returns:
            None
        Raises:
            RuntimeError: Invalid type.
        '''
        types = {'recieved': 1,
                 'filled': 2,
                 'num_recieved': 3}
        
        if type in types:
            self.send('^PT'+chr(types[type]))
        else:
            raise RuntimeError('Invalid type.')
            
    def print_start_command(self, command):
        '''Set print command
        
        Args:
            command: the type of command you desire.
        Returns:
            None
        Raises:
            RuntimeError: Command too long.
        '''
        size = len(command)
        if size > 20:
            raise RuntimeError('Command too long')
        n1 = size/10
        n2 = size%10
        self.send('^PS'+chr(n1)+chr(n2)+command)
    
    def received_char_count(self, count):
        '''Set recieved char count limit
        
        Args:
            count: the amount of received characters you want to stop at.
        Returns:
            None
        Raises:
            None
        '''
        n1 = count/100
        n2 = (count-(n1*100))/10
        n3 = (count-((n1*100)+(n2*10)))
        self.send('^PC'+chr(n1)+chr(n2)+chr(n3))
        
    def select_delim(self, delim):
        '''Select desired delimeter
        
        Args:
            delim: The delimeter character you want.
        Returns:
            None
        Raises:
            RuntimeError: Delimeter too long.
        '''
        size = len(delim)
        if size > 20:
            raise RuntimeError('Delimeter too long')
        n1 = size/10
        n2 = size%10
        self.send('^SS'+chr(n1)+chr(n2))
        
    def select_obj(self, name):
        '''Select an object
        
        Args:
            name: the name of the object you want to select
        Returns:
            None
        Raises:
            None
        '''
        self.send('^ON'+name+chr(0))
    
    def insert_into_obj(self, data):
        '''Insert text into selected object.
        
        Args:
            data: The data you want to insert.
        Returns:
            None
        Raises:
            None
        '''
        if not data:
            data = ''
        size = len(data)
        n1 = size%256
        n2 = size/256
            
        self.send('^DI'+chr(n1)+chr(n2)+data)
    
    def select_and_insert(self, name, data):
        '''Combines selection and data insertion into one function
        
        Args:
            name: the name of the object you want to insert into
            data: the data you want to insert
        Returns:
            None
        Raises:
            None
        '''
        self.select_obj(name)
        self.insert_into_obj(data)
    
    
