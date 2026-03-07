from radon.complexity import cc_visit

def compute_complexity(code):

    try:
        blocks = cc_visit(code)

        if not blocks:
            return 0

        complexity = sum([b.complexity for b in blocks]) / len(blocks)

        return complexity

    except:
        return 0