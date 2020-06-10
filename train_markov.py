import markovify


def main():
    with open('data/train_data.txt') as f:
        train_data = f.readlines()

    for i in range(1, 4):
        print(str(i))
        model = None
        for line in train_data:
            line_model = markovify.Text(line, state_size = i)
            if model:
                model = markovify.combine(models = [model, line_model])
            else:
                model = line_model
        model.compile(inplace = True)
        model_json = model.to_json()
        with open('models/{}-order_markov.txt'.format(i), 'w') as output_file:
            output_file.write(model_json)

if __name__ == '__main__':
    main()
