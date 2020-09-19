from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

class RandomUserAgent():
    
    software_names = [SoftwareName.CHROME.value,SoftwareName.EDGE.value,SoftwareName.OPERA.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value,OperatingSystem.UNIX.value]   

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    @staticmethod
    def get_random():
        return RandomUserAgent.user_agent_rotator.get_random_user_agent()
