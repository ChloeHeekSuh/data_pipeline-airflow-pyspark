from abc import abstractclassmethod, ABC, abstractmethod

#abc — Abstract Base Classes
class AbstractWorkflow(ABC):
    def __init__(self, params, spark):
        self.params = params
        self.spark = spark
        self.steps = {
            # read, transform, save
            'txt' : ['pipeline_read_txt', 'pipeline_transform_txt', 'pipeline_save_txt']

        }

    @abstractmethod
    def run(self):
        pass

    def get_config(self, file_type):
        return self.steps[file_type]