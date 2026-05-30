# -*- coding: utf-8 -*-
from pathlib import Path
from xml.etree import ElementTree as ET
import re
import shutil
import zipfile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

ET.register_namespace("w", W)
ET.register_namespace("a", A)
ET.register_namespace("p", P)
ET.register_namespace("r", R)


def iter_text(el, ns):
    return list(el.iter(f"{{{ns}}}t"))


def read_text(el, ns):
    return "".join((t.text or "") for t in iter_text(el, ns))


def write_text(el, ns, text):
    nodes = iter_text(el, ns)
    if not nodes:
        return
    nodes[0].text = text
    nodes[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for node in nodes[1:]:
        node.text = ""


def revise_docx(src, dst):
    with zipfile.ZipFile(src, "r") as zin:
        payload = {name: zin.read(name) for name in zin.namelist()}

    root = ET.fromstring(payload["word/document.xml"])
    replacements = [
        ("202230211108", "2022302111018"),
        (
            "摒弃传统的TCP协议，基于UDP构建QUIC传输通道，利用QUIC的多流复用（Multi-Streaming）特性，设计了MQTT报文与QUIC流的按优先级映射机制，有效消除了应用层队头阻塞，确保了高优先级控制信令在丢包场景下的实时送达。",
            "以QUIC替代传统TCP/TLS传输路径，基于UDP构建安全传输通道，利用QUIC的多流复用（Multi-Streaming）特性，设计MQTT报文与QUIC流的按优先级映射机制，显著降低连接级队头阻塞对高优先级控制信令的影响。",
        ),
        (
            "上述量化数据充分验证了基于QUIC的架构在弱网环境下的优越性。",
            "上述量化数据验证了基于QUIC的架构在本文实验设定下具备更好的弱网适应能力。",
        ),
        (
            "which effectively eliminates the head of line blocking at the application layer and ensures the real-time delivery of high-priority control signaling in packet loss scenarios.",
            "which significantly reduces the impact of connection-level head-of-line blocking on high-priority control signaling in packet loss scenarios.",
        ),
        (
            "The above quantitative data fully verifies the superiority of the QUIC-based architecture in the weak network environment.",
            "The quantitative results show that the QUIC-based architecture provides better weak-network adaptability under the experimental settings of this study.",
        ),
        (
            "从传输层根除队头阻塞与连接僵化问题。",
            "缓解传统TCP传输中连接级队头阻塞与连接僵化带来的影响。",
        ),
        (
            "这一特性从根本上为解决MQTT的队头阻塞问题提供了物理基础。最后，QUIC引入了连接ID（Connection ID, CID）机制来标识连接上下文。当移动设备在Wi-Fi与4G网络间横向切换导致IP地址变更时，只要数据包头部的CID保持一致，通信即可无缝延续，彻底解决了TCP基于四元组的“连接僵化”难题。",
            "这一特性为缓解MQTT在单连接上传输时的队头阻塞问题提供了重要基础。最后，QUIC引入了连接ID（Connection ID, CID）机制来标识连接上下文。当移动设备在Wi-Fi与4G网络间横向切换导致IP地址变更时，只要数据包头部的CID保持一致，通信即可在路径验证后延续，从而有效缓解TCP基于四元组绑定带来的“连接僵化”难题。",
        ),
        (
            "从根本上消除了应用层队头阻塞。",
            "从而显著降低单一连接内丢包重传对高优先级报文的阻塞影响。",
        ),
        (
            "从应用层彻底消除了大包阻塞心跳包的队头阻塞现象。",
            "显著降低了大包重传对心跳包和控制信令的阻塞影响。",
        ),
        (
            "为了彻底解决 TCP 协议的队头阻塞（Head-of-Line Blocking）问题",
            "为了缓解 TCP 协议的连接级队头阻塞（Head-of-Line Blocking）问题",
        ),
        (
            "系统彻底摒弃了原生 MQTT 基于固定时钟的保活机制",
            "系统不再采用原生 MQTT 基于固定时钟的保活机制",
        ),
        (
            "高并发处理能力：基于Erlang/OTP的轻量级Actor模型，单节点服务端应支持不低于 10,000 个并发长连接。在并发量达到峰值时，单节点消息吞吐量（TPS）应不低于 45,000 条/秒，且系统整体内存占用率不得超过物理内存的 70%。",
            "高并发处理能力：基于Erlang/OTP的轻量级Actor模型，单节点服务端应支持不低于 10,000 个并发长连接。在基准网络环境且并发量达到峰值时，单节点消息吞吐量（TPS）应不低于 45,000 条/秒，且系统整体内存占用率不得超过物理内存的 70%。",
        ),
        (
            "在同等弱网环境下，本系统的 P99 延迟控制在 386 ms，成功从应用层消除了队头阻塞现象[37][38]。",
            "在同等弱网环境下，本系统的 P99 延迟控制在 386 ms，显著削弱了弱网丢包对高优先级信令投递的阻塞影响[37][38]。",
        ),
        (
            "能够有效区分随机丢包与拥塞丢包[36]。在 5% 丢包率下，其 TPS 仍可维持在 31,000 左右，即使丢包率达到10%，亦能保持 15,000 TPS ，吞吐量衰减率远低于 TCP 方案。这充分验证了本系统在弱网环境下对信道带宽的高效利用能力。",
            "在弱网场景中能够更平稳地维持发送速率[36]。在 5% 丢包率下，其 TPS 仍可维持在 31,000 左右，即使丢包率达到10%，亦能保持 15,000 TPS，吞吐量衰减率低于 TCP 方案。该结果表明本系统在弱网环境下具有较好的信道利用能力。",
        ),
        (
            "大大降低了无效网络唤醒次数，也充分验证了其在降低移动终端驻留功耗上的巨大价值。",
            "明显降低了无效网络唤醒次数，也说明该机制有助于降低移动终端驻留功耗。",
        ),
        (
            "如图6.8所示，采用传统 C/C++ 共享内存架构的 Mosquitto 在遭遇畸形报文时发生底层指针溢出，导致全局进程崩溃，TPS 瞬间跌零，经历了长达十余秒的重启与连接重建期。而本系统中处理恶意报文的单个 Erlang Session 进程在发生越界时，立即抛出匹配异常并被监督树隔离销毁（占用句柄瞬间回收）；由主 Router 进程和其余正常用户组成的系统主干保持平稳运行，全局 TPS 曲线依旧维持在 48,500 的高位，未出现任何性能凹陷。该测试直观且有力地证实了系统具备极强的进程级故障隔离与全局高可用性。",
            "如图6.8所示，在本实验配置下，对照组在畸形报文持续注入时出现明显吞吐下降，并需要经历服务恢复与连接重建过程。相比之下，本系统中处理异常报文的单个 Erlang Session 进程会抛出匹配异常并由监督树隔离回收；由主 Router 进程和其余正常用户组成的系统主干保持平稳运行，全局 TPS 曲线仍维持在 48,500 附近，未出现明显性能凹陷。该测试说明系统具备较好的进程级故障隔离能力与全局高可用性。",
        ),
        (
            "从应用层彻底消除了队头阻塞问题。",
            "显著降低了队头阻塞对高优先级报文的影响。",
        ),
        (
            "从根本上打破了 TCP 的连接僵化限制。",
            "有效缓解了 TCP 四元组绑定带来的连接僵化限制。",
        ),
        (
            "充分验证了该架构在移动物联网及即时消息领域所具有的显著工程应用价值。",
            "表明该架构在移动物联网及即时消息领域具有一定工程应用价值。",
        ),
    ]

    for p in root.iter(f"{{{W}}}p"):
        old_text = read_text(p, W)
        new_text = old_text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        if new_text != old_text:
            write_text(p, W, new_text)

    payload["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in payload.items():
            zout.writestr(name, data)


def revise_pptx(src, dst):
    with zipfile.ZipFile(src, "r") as zin:
        payload = {name: zin.read(name) for name in zin.namelist()}

    replacements = [
        ("传统MOTT over TCP", "传统 MQTT over TCP"),
        (
            "即时消息技术已渗透至工业物联网、车联网等关键领域，设备面临高丢包、高RTT抖动、频繁基站切换的恶劣弱网环境",
            "工业物联网、车联网等场景中，终端常处于高丢包、高RTT抖动、频繁基站切换的弱网环境。",
        ),
        (
            "传统 MQTT over TCP在弱网环境下存在固有缺陷，无法满足低延迟、高可靠的通信需求",
            "传统 MQTT over TCP 在弱网环境下存在连接级队头阻塞、重连成本高等问题，难以稳定满足低延迟通信需求。",
        ),
        (
            "基于QUIC协议重构传输层架构，构建一套能够在弱网环境下保持高可靠、低延迟的消息分发机制，为弱网环境提供新型通信基础设施支撑",
            "基于 QUIC 重构传输层，并与 MQTT 消息模型结合，提升弱网环境下的消息投递稳定性与实时性。",
        ),
        (
            "TCP有序字节流机制导致单包丢失阻塞后续所有数据交付，高优先级控制信令实时性无法保障。在弱网环境下该问题尤为突出，严重影响端到端传输效率",
            "TCP 有序字节流中单包丢失会阻塞后续数据交付，高优先级控制信令的实时性受影响。",
        ),
        (
            "固定心跳机制无法适配网络RTT剧烈波动，易造成误判断连，增加终端无效功耗。频繁重连还会进一步加剧网络拥塞，形成恶性循环",
            "固定心跳难以适配 RTT 剧烈波动，容易误判断连并触发无效唤醒与重连。",
        ),
        (
            "TCP连接与IP四元组强绑定，基站切换导致IP变更时连接中断，重连耗时严重。移动场景下平均重连耗时可达数秒，严重影响用户体验",
            "TCP 连接依赖 IP 四元组，网络切换导致 IP 变化时需要重建连接，业务恢复耗时明显。",
        ),
        (
            "1.接入网关层：承接海量并发握手与 QUIC/TLS 1.3 协议解析2.会话维护层：基于 Actor 模型实现进程级状态隔离；负责 MQTT 生命周期维护管理3.消息分发层：基于 ETS 内存表的前缀树实现应用层主题匹配与报文投递4.基础设施层：利用 Redis 缓存与数据库存储离线消息及订阅关系，为业务提供持久化存储支撑",
            "1. 接入网关层：并发握手、QUIC/TLS 1.3 解析\n2. 会话维护层：Actor 进程隔离、MQTT 生命周期管理\n3. 消息分发层：ETS 前缀树主题匹配与报文投递\n4. 基础设施层：Redis 与数据库支撑离线消息、订阅关系持久化",
        ),
        (
            "三级流映射模型：通过流映射器拦截所有 MQTT 报文，根据报文类型与 QoS 等级，动态分配不同的 QUIC 物理通道，打破传统 TCP 单一 FIFO 队列的物理限制，解决队头阻塞问题",
            "三级流映射模型：依据 MQTT 报文类型、QoS 与业务优先级，将控制信令、普通消息、大包数据映射至不同 QUIC Stream，降低连接级队头阻塞影响。",
        ),
        (
            "1.控制指令优先：强制实现控制流与数据流的物理隔离，使业务大包的重传退避不再波及信令传输2.抑制伪断连现象：即使业务流因拥塞导致缓冲区暂停，关键心跳仍能准时送达，保障弱网环境下的长连接稳定性",
            "1. 控制指令优先：业务大包重传不再直接挤占信令传输\n2. 抑制伪断连：业务流拥塞时，关键心跳仍可独立投递",
        ),
        (
            "1.模型选型：针对移动网络 RTT 的高频毛刺与非高斯抖动特性，建立一维卡尔曼滤波模型，实时采集底层 RTT 采样值以平滑处理网络抖动",
            "1. 模型选型：针对移动网络 RTT 高频毛刺与突发抖动，建立一维卡尔曼滤波模型，平滑底层 RTT 采样值",
        ),
        (
            "2.动态阈值：高抖动期自动拉长超时宽容度防误杀，平稳期收紧阈值保敏锐，有效降低无效唤醒功耗",
            "2. 动态阈值：高抖动期放宽超时阈值，平稳期收紧阈值，降低误判断连与无效唤醒",
        ),
        (
            "脱离 IP 强依赖，利用 QUIC Connection ID 作为连接唯一标识符，在内存中构建基于 ETS 的无锁并发路由表。IP 物理变更时，底层网关以 O(1) 复杂度提取 CID 并重组路由路径",
            "利用 QUIC Connection ID 作为连接标识，在 ETS 中维护 CID 到会话进程的路由关系。\nIP 发生物理变更时，网关基于 CID 完成路径验证与路由更新，上层 MQTT 会话保持连续。",
        ),
        (
            "1.仿真环境：基于 Linux 内核级的 TC (Traffic Control) 框架联合 NetEm 模块，在网关侧精准构建可控、可复现的弱网损伤环境",
            "1. 仿真环境：TC + NetEm 在网关侧注入可控、可复现的弱网损伤",
        ),
        (
            "2.对比基准：选取传统 TCP 标杆实现（Mosquitto）作为实验对照组",
            "2. 对比基准：以 Mosquitto over TCP 作为实验对照组",
        ),
        (
            "基准满载：无人工损伤的基准环境，测定系统资源开销和鲁棒性。渐进劣化：丢包率 0%→10% 阶梯递增，测定吞吐量（TPS）随信道质量下降的衰减趋势。恶劣弱网：5% 丢包 + 200ms 延时抖动，模拟工业经典弱网环境，验证端到端长尾延迟表现。动态拓扑：RTT 在 50ms 至 500ms 剧烈抖动与物理 IP 变更，验证自适应心跳的稳定性及 CID 无缝迁移能力",
            "基准满载：无人工损伤，观察资源开销与稳定性\n渐进劣化：丢包率 0%→10%，观察 TPS 衰减\n恶劣弱网：5% 丢包 + 200ms 延迟，观察 P99 延迟\n动态拓扑：RTT 50ms→500ms + IP 变更，验证心跳与 CID 迁移",
        ),
        (
            "在5%丢包，200ms延迟下，Mosquitto 的 P99 延迟高达 2095 ms，而本系统的 P99 延迟控制在 386 ms 在同等弱网环境下，本系统的 P99 延迟远低于 TCP 方案 ，成功从应用层消除了队头阻塞现象",
            "5% 丢包、200ms 延迟下：\nMosquitto P99 = 2095 ms\n本系统 P99 = 386 ms\n结论：多流映射显著降低弱网丢包对高优先级信令的阻塞影响。",
        ),
        (
            "在 RTT 50-500ms 剧烈波动的环境下， 1,000 个并发设备持续保活 1 小时，Mosquitto 各统计区间约为 2400 次触发，而本系统仅产生了少量次数的真实断线重连本系统相较TCP方案大大降低了无效的网络唤醒次数，验证了其在降低移动终端驻留功耗上的巨大价值",
            "RTT 50-500ms 波动、1,000 并发设备持续保活 1 小时：\n固定心跳触发大量无效唤醒；本系统主要保留真实断线重连。\n结论：动态阈值降低了误判断连与终端驻留功耗。",
        ),
        (
            "在基准环境下，移动端设备从 源 IP: A 物理切换至 源 IP: B时，Mosquitto 断线重连耗时 3150 ms，而本系统仅需 48 ms即完成了重连过程本系统相较TCP方案对底层网络切换无感知，实现了中断时间减少 98.4% 的高效网络无感迁移",
            "移动端从源 IP A 切换至源 IP B：\nMosquitto 恢复耗时 3150 ms\n本系统路径验证与业务恢复耗时 48 ms\n结论：CID 迁移将中断时间缩短 98.4%。",
        ),
        (
            "1. 资源代价：14核CPU占用率略高15%（用户态解密开销），但64GB内存占用率降低30%（Erlang 独立 GC 优势）。2. 高可用性：恶意报文攻击下，系统全局 TPS 曲线始终维持在48,500高位平稳，未出现凹陷。",
            "资源代价：CPU 占用率高约 15 个百分点，主要来自用户态加解密与拥塞控制。\n内存收益：64GB 环境下内存占用降低约 30%，受益于 Erlang 轻量进程与独立 GC。\n鲁棒性：畸形报文注入时，全局 TPS 维持在 48,500 附近，未出现明显凹陷。",
        ),
        (
            "在JMeter 发起 10,000 并发负载，物理丢包率从 0% 阶梯递增至 10% ，Mosquitto 在丢包率达到 2% 时 TPS 骤降至 12,000 左右，并随丢包率递增持续快速下滑，而本系统即使在丢包率达到10%时，亦能保持 15,000 TPS本系统的吞吐量衰减率远低于 TCP 方案，验证了本系统在弱网环境下对信道带宽的高效利用能力",
            "10,000 并发负载、丢包率 0%→10%：\nMosquitto 在 2% 丢包时降至约 12,000 TPS，并继续快速下滑。\n本系统在 5% 丢包时约 31,000 TPS，10% 丢包时仍约 15,000 TPS。\n结论：弱网下吞吐衰减更平缓。",
        ),
        (
            "传输层重构基于 QUIC 多流映射彻底根除队头阻塞基于 QUIC CID 机制实现连接无缝迁移自适应保活卡尔曼滤波平滑 RTT 抖动，动态阈值规避弱网误判无锁并发架构ETS 无锁路由表 + Actor 模型，实现大规模会话高效管理",
            "传输层重构：QUIC 多流映射降低队头阻塞影响\n连接迁移：基于 QUIC CID 实现路径切换下的会话连续\n自适应保活：卡尔曼滤波平滑 RTT，动态阈值降低弱网误判\n并发架构：ETS 路由表 + Actor 模型支撑大规模会话管理",
        ),
        (
            "引入 eBPF 内核旁路技术,将加解密计算卸载至内核层以进一步降低 CPU 开销探索 MP-QUIC 多路径传输，聚合多网卡带宽，进一步提升吞吐与可靠性",
            "引入 eBPF / SmartNIC 等旁路或卸载技术，降低 QUIC 用户态计算开销\n探索 MP-QUIC 多路径传输，聚合 Wi-Fi 与蜂窝链路提升可靠性",
        ),
    ]

    for name in list(payload):
        if not re.match(r"ppt/slides/slide\d+\.xml$", name):
            continue
        root = ET.fromstring(payload[name])
        for sp in root.findall(".//p:sp", {"p": P}):
            old_text = read_text(sp, A)
            new_text = old_text
            for old, new in replacements:
                new_text = new_text.replace(old, new)
            if new_text != old_text:
                write_text(sp, A, new_text)
        payload[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in payload.items():
            zout.writestr(name, data)


def extract_docx(path, out_path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    with open(out_path, "w", encoding="utf-8") as f:
        for i, p in enumerate(root.iter(f"{{{W}}}p"), 1):
            text = read_text(p, W).strip()
            if not text:
                continue
            style = ""
            ppr = p.find(f"{{{W}}}pPr")
            if ppr is not None:
                pstyle = ppr.find(f"{{{W}}}pStyle")
                if pstyle is not None:
                    style = pstyle.attrib.get(f"{{{W}}}val", "")
            f.write(f"{i:04d}\t{style}\t{text}\n")


def extract_pptx(path, out_path):
    with zipfile.ZipFile(path) as z, open(out_path, "w", encoding="utf-8") as f:
        names = sorted(
            [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)),
        )
        for idx, name in enumerate(names, 1):
            root = ET.fromstring(z.read(name))
            f.write(f"--- Slide {idx} ({name}) ---\n")
            for sp in root.findall(".//p:sp", {"p": P}):
                text = read_text(sp, A).strip()
                if text:
                    f.write(text + "\n")
            f.write("\n")


def main():
    cwd = Path(".")
    original_docx = next(p for p in cwd.glob("*.docx") if "终稿修订版" not in p.name)
    original_pptx = next(p for p in cwd.glob("*.pptx") if "终稿修订版" not in p.name)
    revised_docx = cwd / f"{original_docx.stem}_终稿修订版.docx"
    revised_pptx = cwd / f"{original_pptx.stem}_终稿修订版.pptx"

    revise_docx(original_docx, revised_docx)
    revise_pptx(original_pptx, revised_pptx)
    extract_docx(original_docx, cwd / "doc_extract.txt")
    extract_pptx(original_pptx, cwd / "ppt_extract.txt")
    extract_docx(revised_docx, cwd / "doc_revised_extract.txt")
    extract_pptx(revised_pptx, cwd / "ppt_revised_extract.txt")
    print(revised_docx)
    print(revised_pptx)
    print("doc_extract.txt")
    print("ppt_extract.txt")
    print("doc_revised_extract.txt")
    print("ppt_revised_extract.txt")


if __name__ == "__main__":
    main()
