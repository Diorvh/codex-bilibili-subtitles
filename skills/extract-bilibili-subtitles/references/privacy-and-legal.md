# Privacy, platform terms, and copyright boundary

This reference explains the project's intended safeguards. It is not legal advice and cannot determine whether a particular use is lawful.

## Platform-contract risk

Bilibili's user agreement should be checked before every material use because platform terms can change. As reviewed on 2026-08-19, the agreement described the service as non-commercial absent written consent and prohibited obtaining platform services, content, or data through robots, spiders, crawlers, automatic programs, or scripts without written permission. That creates a meaningful terms-of-service and account-enforcement risk even when a user can watch the video normally.

Source: [Bilibili User Agreement](https://www.bilibili.com/blackboard/user-rule-linux.html?night=1&padding=0), especially the sections governing non-commercial use and automated collection.

Therefore:

- do not say the workflow is “basically risk-free”;
- prefer content owned by the user or content for which the user has explicit permission;
- keep requests isolated, manual, and low-frequency;
- stop if the platform presents an access challenge or denial;
- do not create evasion, stealth, account-rotation, or bulk-collection features.

## Copyright risk

A subtitle or transcript may contain copyrighted expression independent of the software used to retrieve it. Access does not automatically confer the right to reproduce, publish, distribute, translate, or commercialize the full transcript.

Article 24 of the Copyright Law of the People's Republic of China includes limited circumstances such as personal study or research and appropriate quotation, subject to attribution and non-interference conditions. Whether an actual use qualifies is fact-specific.

Source: [Copyright Law of the People's Republic of China](https://www.npc.gov.cn/c2/c30834/202011/t20201119_308796.html), Article 24.

Lower-risk patterns generally include private, limited processing of content the user owns or is authorized to use. Higher-risk patterns include publishing a complete third-party transcript, monetizing it, building a searchable corpus, or substituting for the original work.

## Repository policy

The MIT License covers only this repository's original code and documentation. It does not license:

- Bilibili videos or subtitle tracks;
- creators' speech, scripts, images, music, or trademarks;
- browser Cookies or account data;
- yt-dlp or any other third-party dependency.

The public repository must contain no extracted third-party subtitle, video, audio, or browser data. Synthetic fixtures must be written specifically for testing.

## Privacy design

- Credentials are never requested through chat or command-line options.
- Cookie files are not accepted or exported.
- The user initiates authenticated extraction in their own terminal.
- Browser Cookies are read by yt-dlp in process, subject to yt-dlp and operating-system behavior.
- The plugin does not run a remote service and does not upload subtitle output.
- Verbose request logging is discouraged.

yt-dlp documents that exported Cookie files may include Cookies for every site in the browser profile and therefore require strong protection. This project avoids that export workflow. See the [yt-dlp FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ).

## Open-source hosting

Publishing neutral source code is distinct from publishing copied subtitle content, but repository hosts can still remove content that violates their policies or receives a valid legal complaint. Contributors should review [GitHub's Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) and [DMCA Takedown Policy](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy).

## Stop conditions

Do not proceed when:

- the user asks to bypass access controls or conceal automation;
- credentials do not belong to the user;
- the user wants a bulk archive or complete third-party transcript corpus;
- the intended use is redistribution or commercialization without rights clearance;
- the platform rejects the request or demands a challenge the normal browser session cannot satisfy;
- applicable law, employer policy, school policy, or platform terms prohibit the action.
