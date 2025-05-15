import numpy as np
import random
def parse_multi_choice_response(response, all_choices, index2ans):
    """
    Parse the prediction from the generated response.
    Return the predicted index e.g., A, B, C, D.
    """
    for char in [',', '.', '!', '?', ';', ':', "'"]:
        response = response.strip(char)
    response = " " + response + " " # add space to avoid partial match

    index_ans = True
    ans_with_brack = False
    candidates = []
    for choice in all_choices:  # e.g., (A) (B) (C) (D)
        if f'({choice})' in response:
            candidates.append(choice)
            ans_with_brack = True
    if len(candidates) == 0:
        for choice in all_choices: # e.g., A B C D
            if f' {choice} ' in response:
                candidates.append(choice)

    # if all above doesn't get candidates, check if the content is larger than 5 tokens and try to parse the example
    if len(candidates) == 0 and len(response.split()) > 5:
        for index, ans in index2ans.items():
            if ans.lower() in response.lower():
                candidates.append(index)
                index_ans = False # it's content ans.

    # print("haha",candidates)
    if len(candidates) == 0:  # still not get answer, randomly choose one.
        pred_index = 'None' + str(random.randint(0,255))
    elif len(candidates) > 1:
        start_indexes = []
        if index_ans:
            if ans_with_brack:
                for can in candidates:
                    index = response.rfind(f'({can})')
                    start_indexes.append(index) # -1 will be ignored anyway
                # start_indexes = [generated_response.index(f'({can})') for can in candidates]
            else:
                for can in candidates:
                    index = response.rfind(f" {can} ")
                    start_indexes.append(index)
        else:
            for can in candidates:
                index = response.lower().rfind(index2ans[can].lower())
                start_indexes.append(index)
        # get the last one
        pred_index = candidates[np.argmax(start_indexes)]
    else: # if only one candidate, use it.
        pred_index = candidates[0]

    return pred_index



def multiple_choice_checker(
        gt : str,
        pred : str
) -> bool:
    if len(pred) > 50:
        pred = pred[-10:]
    pred = pred.split(',')
    gt   = gt.upper().split(',')

    # pred = (#)
    jury = set([parse_multi_choice_response(_, ["A","B","C","D"] , {}) for _ in pred])
    std  = set([parse_multi_choice_response(_, ["A", "B", "C", "D"], {}) for _ in gt])
    # print(jury,std)
    return jury == std
if __name__ == "__main__":
    print(multiple_choice_checker('B',"According to Figure 1, which details \"Iraq's bloody toll\" with a focus on the massive number of civilian and other deaths, the predominant theme is one of immense loss of life and tragedy. The graph visually represents the scale of death over several years. Let's analyze the options in this context:\n\n(A) The fear of blood: While \"bloody toll\" is in the title and red is a dominant color, the graph itself quantifies deaths. Fear of blood is a specific phobia or immediate reaction to violence, but the graph presents the aftermath and scale of death, which is broader than just the fear of blood.\n\n(B) The grief for death: Figure 1 overwhelmingly presents statistics about death. The sheer number of casualties (e.g., 113,726 civilian deaths) directly points to widespread loss. Grief is the natural and profound emotional response to such extensive death. The purpose of such a graphic is often to convey the human cost, which is closely associated with grief.\n\n(C) The amazement at quantity: The numbers are indeed shockingly large, and one might be amazed or stunned by the scale. However, \"amazement\" alone doesn't fully capture the emotional gravity of what these quantities represent – human lives lost. It's a more intellectual or initial reaction.\n\n(D) The indifference of society: Figure 1, by its nature as an informative graphic likely published to raise awareness, aims to combat indifference rather than depict it as a predominant emotion stemming from the facts. It highlights a serious issue, implicitly calling for attention and concern.\n\nConsidering the central message of Figure 1 is the staggering number of deaths and the tragic human cost of the conflict, the most predominant emotion that Figure 1 would suggest for a related Figure 2 (which would presumably depict the human aspect of this toll) is grief. The data in Figure 1 is a quantifiable representation of events that would cause widespread grief.\n\nThe final answer is $\\  B  $."))