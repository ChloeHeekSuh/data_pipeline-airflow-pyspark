from pipeline_workflow.abstract_workflow import AbstractWorkflow
from pipeline_step.pipeline_step_loader import PipelineStepLoader
import pkgutil # helps python script get on the class path
import pipeline_custom

class DefaultWorkflow(AbstractWorkflow):
    def __init__(self, params, spark):
        # AbstractWorkflow class를 받아서 연장. 상속
        super().__init__(params, spark)

    def run(self):
        file_type = self.params.args['file_type']
        steps = super().get_config(file_type)
        # After read the txt, we are gonna have a dataframe 
        # return dataframe which proccess one by one
        df = None
        for node in steps:
            custom_steps = set(
                [modname for importer, modname, ispkg in pkgutil.iter_modules(pipeline_custom.__path__)]
            )
        # let's code below variable 'temp_cls, params' in the Pipeline_Step_Loader class
        temp_cls, params = PipelineStepLoader.get_class(node, self.params, custom_steps=custom_steps)
        df = temp_cls.run(self.spark, params, df)

        # 노드가 한번 돌아갈 때마다 dataframe이 계속 덮어씌워진다.