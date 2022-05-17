class LevelMeter extends AudioWorkletProcessor
{
    constructor()
    {
        super();
        this.idx = 0;
        this.ch = 0;
        this.i = 0;
        this.input = null;
        this.output = null;
        this.channels = null;
        this.samples = null;
        this.max = 0;
        this.tmp = 0;
    }
    static get parameterDescriptors()
    {
        return [
        {
            name: "id",
            defaultValue: 0,
            minValue: 0,
            maxValue: 9999,
            automationRate: "k-rate"
        }];
    }
    process(inputs, outputs, parameters)
    {
        const sourceLimit = Math.min(inputs.length, outputs.length);
        for (this.idx = 0; this.idx < sourceLimit; ++this.idx)
        {
            this.input = inputs[this.idx];
            this.output = outputs[this.idx];
            this.channels = Math.min(this.input.length, this.output.length);
            for (this.ch = 0; this.ch < this.channels; ++this.ch)
            {
                this.samples = this.input[this.ch].length;
                this.max = 0;
                this.tmp = 0;
                for (this.i = 0; this.i < this.samples; ++this.i)
                {
                    this.tmp = Math.abs(this.input[this.ch][this.i]);
                    if (this.tmp > this.max) { this.max = this.tmp; }
                }
                this.port.postMessage(JSON.stringify(
                {
                    "origin": "LevelMeter",
                    "id": parameters["id"][0],
                    "ch": this.ch,
                    "value": this.max,
                }));
            }
        };
        return true;
    };
}
registerProcessor("LevelMeter", LevelMeter);