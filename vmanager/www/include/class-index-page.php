<?php

require_once dirname( __FILE__ ) . '/class-vmanager.php';

class IndexPage extends Vmanager{

	public function vmInfoTable(){
		$vms = $this->vmInfo();
		?>
		<table id='vms'>
			<tr>
				<th title='Имя VM'>VM</th>
				<th title="Статус: вкл/откл">State</th>
				<th title='High Availability'>HA</th>
				<th title="Гипервизор, на котором запущена VM">Host</th>
				<th title='RSS RAM используемая VM на гипервизоре, МБ'>VM RAM, Мb</th>
				<th title='Свободно RAM на гипервизоре, МБ'>Host Free RAM, Mb</th>
				<th>Дни бекапа</th>
				<th>Последний бекап</th>
				<th title="Проверка статуса бекапа по логу ok/fail/-(если лог удален)">Статус по логу</th>
			</tr>
				<?php
				foreach ($vms as $vm) {
					$cell = $this->prepareCellValue( $vm );
					echo "<tr id='{$cell[0]}'>";
					foreach ($cell as $v)
						echo "<td>{$v}</td>";
					echo '</tr>';
				}
				?>
		</table>
		<?php
	}

	private $month = array("Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Сен", "Окт", "Ноя", "Дек");
	private function numberToMonth($month_number){
		return $this->month[ (int)$month_number - 1 ];
	}

	/**
	* @ return array
	**/
	private function prepareCellValue ( $vm ){
		$data = explode(' ', $vm);
		$vm_name = $data[0];
		$data[1] = $this->prepareStateCell( $data[1], $vm_name );
		$data[2] = $this->prepareAutoStartCell( $data[2], $vm_name );
		$data[4] = number_format($data[4], 0, '.', ' '); // vm mem
		$data[5] = number_format($data[5], 0, '.', ' '); // host free mem
		$data[6] = $this->prepareBackupDayCell( $data[6], $vm_name);
		if( $data[7] != '-' ){
			$d = explode('-', $data[7]); // last backup day
			$month = $this->numberToMonth( $d[0] );
			$d = explode('_', $d[1]);
			$data[7] = $d[0] . " ". $month . " " . $d[1];
		}
		return $data;
	}

	private function prepareStateCell( $value, $vm_name ){
		switch($value){
		case 'running':
			$img = '<img class="power-state" id="power-state-'.$vm_name.'" src="img/green.png" vmstate="'.$value.'">';
			break;
		case 'shut_off':
			$img = '<img class="power-state" id="power-state-'.$vm_name.'" src="img/red.png" vmstate="'.$value.'">';
			break;
		default:
			$img = $data[1];
		}
		$img .= '<ul class="power-buttons">';
		$img .= '<li>&#9662; <ul>';
		$img .= 	'<li title="gracefully on/off '.$vm_name.'"><img class="power-button" src="img/power_button.png" vmname="'.$vm_name.'"></li>';
		$img .= 	'<li title="destroy '.$vm_name.'"><img class="destroy-button" src="img/destroy_button.png" vmname="'.$vm_name.'"></li>';
		$img .= 	'<li title="hard reset '.$vm_name.'"><img class="reset-button" src="img/reset_button.png" vmname="'.$vm_name.'"></li>';
		$img .= '</ul></li></ul>';
		return $img;
	}

	private function prepareAutoStartCell( $value, $vm_name ){
		$checked = ("on"==$value) ? "checked":"";
		$id = 'autostart_' . $vm_name;
		return
		'<div class="onoffswitch">'.
			'<input type="checkbox" class="onoffswitch-checkbox autostart-checkbox" '.
				'id="'.$id.'" autocomplete="off"  '.$checked.' vmname="'.$vm_name.'">'.
			'<label class="onoffswitch-label" for="'.$id.'">'.
			'<span class="onoffswitch-inner"></span>'.
			'<span class="onoffswitch-switch"></span>'.
			'</label>'.
		'</div>';
	}

	private function prepareBackupDayCell( $value, $vm_name ){
		return $value.'&nbsp;&nbsp;&nbsp;<a class="backup-button" vmname="'.$vm_name.'" title="Ручной бекап">backup now</a>';
	}
}
?>
