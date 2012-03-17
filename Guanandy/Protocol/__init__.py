"""
This define de protocol used to exchange message from/to teacher/student
"""


# From student to teacher
registerStudent = {'action': 'registerStudent',
                  }


# From teacher to student

sendScreen = {'action': 'sendScreen',
             }

lockScreen = {'action': 'lockScreen',
             }

shareFile = {'action': 'shareFile',
             'file': '',
            }

shareWebPage = {'action': 'shareWebPage',
                'url': '',
                }

sendMessage = {'action': 'sendMessage',
               'message': '',
              }

openApplication = {'action': 'openApplication',
                   'application': '',
                  }

turnOff = {'action': 'turnOff',
          }

# Both direction
callAttention = {'action': 'callAttention',
                }
