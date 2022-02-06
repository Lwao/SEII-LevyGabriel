var value_;
var result_;

function button_(num)
{
    value_ = document.calc.screen.value += num;
}

function reset_()
{
    document.calc.screen.value = '';
}

function compute_()
{
    result_ = eval(value_);
    document.calc.screen.value = result_.toLocaleString('pt-br');
}