from pipeline_step.pipeline_step import PipelineStep

class PipelineReadTxt(PipelineStep):
    def __init__(self):
        super().__init__()
        print('Read File')

    def run(self, spark, params, df):
        path = params.args['input_path']
        # TODO, comment this line off when debug is complete.
        spark.read.option('header','true').csv(path).show()
        # change this to a dict and loop through the args['input_options']
        return spark.read.option('header','true').csv(path)