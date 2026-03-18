import argparse
import subprocess
from pathlib import Path

from janim.typing import t_

PREAMBLE = t_(
    R'''
    #let parse(x) = {
        let match(..s) = x => s.pos().any(v => repr(x.func()) == v)
        let match-func(..s) = x => s.pos().any(v => x.func() == v)
        let default() = x => true

        let item(x) = (x,)
        let newline(..lines) = ("", ..lines.pos(), "")

        let wraps(child-pars, prefix, suffix) = {
            let len = child-pars.len()
            child-pars.enumerate().map(
                ((i, x)) => {
                    if i == 0 { prefix }
                    x
                    if i == len - 1 { suffix }
                }
            )
        }

        let parsers = (
            match("sequence"),
            x => item({
                let (pars, accum) = x.children.fold(
                    ((), ""),
                    ((pars, accum), child) => {
                        let child-pars = parse(child)
                        for (i, parsed) in child-pars.enumerate() {
                            if type(parsed) == array {
                                if accum.len() != 0 {
                                    pars.push(accum.trim())
                                    accum = ""
                                }
                                pars.push(parsed)
                            } else {
                                accum += parsed
                                if i != child-pars.len() - 1 {
                                    if accum.len() != 0 {
                                        pars.push(accum.trim())
                                    }
                                    accum = ""
                                }
                            }
                        }
                        return (pars, accum)
                    }
                )
                if accum.len() != 0 {
                    pars.push(accum.trim())
                }
                return pars
            }),

            match("parbreak"),
            x => ("", ""),

            match("text"),
            x => item(x.text),

            match("space"),
            x => item(" "),

            match("equation"),
            x => {
                if x.block {
                    newline("{数学公式}")
                } else {
                    item("{数学公式}")
                }
            },

            match("raw"),
            x => {
                if x.block {
                    let lang = x.fields().at("lang", default: "")
                    newline("```" + lang + "\n" + x.text + "\n" + "```")
                } else {
                    item("`" + x.text + "`")
                }
            },

            match("smartquote"),
            x => item("'"),

            match("symbol"),
            x => item(x.text),

            match("styled"),
            x => newline(..parse(x.child)),

            match("block", "box"),
            x => newline(parse(x.body)),

            match("heading"),
            x => newline(..wraps(parse(x.body), "#" * x.depth + " ", "")),

            match("strong"),
            x => wraps(parse(x.body), "*", "*"),

            match-func(enum.item),
            x => newline(..wraps(parse(x.body), "+ ", "")),
            match-func(list.item),
            x => newline(..wraps(parse(x.body), "- ", "")),

            //x => x.fields().at("body", default: none) != none,
            //x => parse(x.body),

            match("metadata", "counter-update", "context", "state-update"),
            x => (),

            default(),
            x => item("#" + repr(x))
            // x => {
            //     "[type:" + repr(type(x)) + ",#" + repr(x) + "]"
            // }
        ).chunks(2)

        let get-parser(x) = {
            for ((cond, parser)) in parsers {
                if cond(x) {
                    return parser
                }
            }
            assert(false, "Impossible")
        }
        get-parser(x)(x)
    }

    #let format-text-tree(tree, indent: 0) = {
        tree.map(x => {
            if type(x) == str {
                " " * indent + x
            } else {
                format-text-tree(x, indent: indent + 4)
            }
        }).join("\n\n")
    }

    // #show: doc => [
    //   #[
    //     #show raw: set text(font: ("Consolas", "Noto Serif CJK SC"))
    //     #box(
    //       stroke: blue,
    //       inset: 8pt,
    //       width: 100%,
    //       radius: 4pt,
    //       raw(format-text-tree(parse(doc)))
    //     )
    //   ]

    //   #doc
    // ]
    #show: doc => [#metadata(format-text-tree(parse(doc))) <plain-text>]
    '''
)


def build_wrapper_content(target_file: Path) -> str:
    removes = [
        '#show: zebraw'
    ]
    filecontent = target_file.read_text(encoding='utf-8')
    for remove in removes:
        filecontent = filecontent.replace(remove, "")
    return f'{PREAMBLE}\n\n{filecontent}'


def extract_plain_text(file_path: str) -> str:
    target_file = Path(file_path).resolve()
    if not target_file.exists():
        raise FileNotFoundError(f'文件不存在: {target_file}')

    try:
        result = subprocess.run(
            [
                'typst',
                'query',
                '-',
                '<plain-text>',
                '--one',
                '--field',
                'value',
            ],
            input=build_wrapper_content(target_file),
            encoding='utf-8',
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.rstrip('\n').strip('"').replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
    except subprocess.CalledProcessError as err:
        stderr = err.stderr.strip() if err.stderr else str(err)
        raise RuntimeError(f'typst query 执行失败: {stderr}') from err


def main(file_path: str) -> None:
    text = extract_plain_text(file_path)
    print(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='输入 .typ 文件路径，例如 draft.typ')
    args = parser.parse_args()
    main(args.file_path)
